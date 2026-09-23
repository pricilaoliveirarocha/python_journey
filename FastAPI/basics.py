from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime, Enum as SqlEnum, String, Text, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from FastAPI.database import Base, SessionLocal, engine, get_db


class TaskStatus(str, Enum):
    """Possíveis estados de uma tarefa."""

    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskRecord(Base):
    """Representação da tabela tasks no PostgreSQL."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(
        SqlEnum(TaskStatus, name="task_status"), default=TaskStatus.pending
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


def initialize_database() -> None:
    """Cria a tabela e inclui exemplos somente quando ela estiver vazia."""

    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        has_tasks = db.scalar(select(TaskRecord.id).limit(1)) is not None
        if not has_tasks:
            db.add_all(
                [
                    TaskRecord(
                        title="Estudar FastAPI",
                        description="Aprender rotas, parâmetros e modelos de resposta.",
                        status=TaskStatus.in_progress,
                        due_date=datetime(2026, 9, 30, 23, 59, tzinfo=timezone.utc),
                    ),
                    TaskRecord(
                        title="Criar uma API de tarefas",
                        description="Consultar tarefas armazenadas no PostgreSQL.",
                        status=TaskStatus.pending,
                    ),
                ]
            )
            db.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Tasks API",
    description="API de exemplo para consultar tarefas.",
    version="1.0.0",
    lifespan=lifespan,
)


class Task(BaseModel):
    """Estrutura retornada ao consultar os detalhes de uma tarefa."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    due_date: datetime | None = None


@app.get("/", tags=["Geral"], summary="Apresenta a API")
async def read_root():
    """Retorna informações básicas e os principais links da API."""

    return {
        "message": "Bem-vindo à Tasks API!",
        "version": app.version,
        "documentation": "/docs",
        "endpoints": {"task_details": "/tasks/{task_id}"},
    }


@app.get(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
    summary="Consulta os detalhes de uma tarefa",
)
async def get_task(
    task_id: int, db: Annotated[Session, Depends(get_db)]
) -> TaskRecord:
    """Busca uma tarefa no PostgreSQL pelo ID."""

    task = db.get(TaskRecord, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {task_id} não encontrada.",
        )

    return task


# Execute na raiz do projeto: uvicorn FastAPI.basics:app --reload
