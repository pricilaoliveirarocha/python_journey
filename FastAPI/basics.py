from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import DateTime, String, Text, select
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, Session, mapped_column

from database import Base, SessionLocal, engine, get_db

API_DESCRIPTION = """
API didática para consultar tarefas armazenadas em um banco PostgreSQL.

## Recursos

* Consulte uma tarefa pelo seu identificador.
* Receba respostas JSON validadas pelo Pydantic.
* Explore e teste as rotas diretamente nesta documentação.
"""

DOCS_URL = "/docs"
REDOC_URL = "/redoc"

OPENAPI_TAGS = [
    {
        "name": "Geral",
        "description": "Informações gerais e links úteis da aplicação.",
    },
    {
        "name": "Tasks",
        "description": "Operações de consulta das tarefas cadastradas.",
    },
]


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
    """Prepara as tabelas e os dados iniciais durante a inicialização."""

    initialize_database()
    yield


app = FastAPI(
    title="Tasks API",
    description=API_DESCRIPTION,
    version="1.0.0",
    openapi_tags=OPENAPI_TAGS,
    docs_url=DOCS_URL,
    redoc_url=REDOC_URL,
    lifespan=lifespan,
)


class Task(BaseModel):
    """Representa os detalhes públicos de uma tarefa."""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Estudar FastAPI",
                "description": "Aprender rotas e modelos de resposta.",
                "status": "in_progress",
                "created_at": "2026-09-22T21:09:10-03:00",
                "due_date": "2026-09-30T20:59:00-03:00",
            }
        },
    )

    id: int = Field(description="Identificador único da tarefa.")
    title: str = Field(description="Título curto da tarefa.")
    description: str = Field(description="Descrição detalhada da tarefa.")
    status: TaskStatus = Field(description="Estado atual da tarefa.")
    created_at: datetime = Field(description="Data e hora de criação.")
    due_date: datetime | None = Field(
        default=None,
        description="Prazo da tarefa, quando definido.",
    )


class RootResponse(BaseModel):
    """Informações básicas para começar a explorar a API."""

    message: str
    version: str
    documentation: str
    alternative_documentation: str
    endpoints: dict[str, str]


class ErrorResponse(BaseModel):
    """Formato padrão das respostas de erro."""

    detail: str = Field(examples=["Tarefa com ID 999 não encontrada."])


@app.get(
    "/",
    response_model=RootResponse,
    tags=["Geral"],
    summary="Apresenta a API",
    description="Retorna a versão da aplicação e links para explorar suas rotas.",
    response_description="Informações e links da API.",
)
async def read_root() -> RootResponse:
    """Apresenta os pontos de entrada da aplicação."""

    return RootResponse(
        message="Bem-vindo à Tasks API!",
        version=app.version,
        documentation=DOCS_URL,
        alternative_documentation=REDOC_URL,
        endpoints={"task_details": "/tasks/{task_id}"},
    )


@app.get(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
    summary="Consulta os detalhes de uma tarefa",
    description=(
        "Busca uma tarefa pelo identificador informado. "
        "Os dados são consultados diretamente no PostgreSQL."
    ),
    response_description="Detalhes da tarefa encontrada.",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Não existe uma tarefa com o ID informado.",
        }
    },
)
async def get_task(
    task_id: Annotated[
        int,
        Path(
            title="ID da tarefa",
            description="Identificador numérico da tarefa no banco de dados.",
            ge=1,
            examples=[1],
        ),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> TaskRecord:
    """Retorna uma tarefa existente ou gera o erro HTTP 404."""

    task = db.get(TaskRecord, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {task_id} não encontrada.",
        )

    return task


# Execute nesta pasta: uvicorn basics:app --reload
