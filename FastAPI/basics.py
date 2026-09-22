# Sobre FastAPI

# FastAPI é um framework moderno e rápido para construir APIs em Python, baseado em anotações de tipo e o modelo de programação assíncrona do Python. Ele permite a criação de APIs com alto desempenho e fácil manutenção, além de fornecer recursos avançados como geração automática de documentação e validação de dados.

from fastapi import FastAPI

app = FastAPI() # Cria uma instância de FastAPI

@app.get("/") # Define uma rota GET para o endpoint raiz
async def read_root():
    return {"message": "Hello world, again =)"} # Retorna uma resposta JSON com uma mensagem da rota raiz

# para rodar a aplicação, use o comando: uvicorn basics:app --reload
