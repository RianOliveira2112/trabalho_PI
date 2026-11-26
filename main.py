import logging

from fastapi import FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import JSONResponse
from mysql.connector import Error as MySQLError

from database import executar_sql

app = FastAPI(title="API de Tutores e Pets — Desenvolvimento Web II")

@app.exception_handler(MySQLError)
def erro_de_banco(request: Request, exc: MySQLError):
    logging.getLogger("uvicorn.error").error("Erro no MySQL: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Não foi possível acessar o banco de dados."},
    )

def representar_tutor(tutor):
    return {
        "id": tutor["id"],
        "nome": tutor["nome"],
        "email": tutor["email"],
        "telefone": tutor["telefone"],
    }

def representar_pet(pet):
    nascimento = pet["data_nascimento"]
    return {
        "id": pet["id"],
        "nome": pet["nome"],
        "especie": pet["especie"],
        "raca": pet["raca"],
        "data_nascimento": nascimento.isoformat() if nascimento else None,
        "tutor": {"id": pet["tutor_id"], "nome": pet["tutor_nome"]},
    }

SQL_PETS = (
    "SELECT p.id, p.nome, p.especie, p.raca, p.data_nascimento, "
    "p.tutor_id, t.nome AS tutor_nome "
    "FROM pets p "
    "INNER JOIN tutores t ON t.id = p.tutor_id"
)

@app.get("/tutores")
def listar_tutores():
    sql = "SELECT id, nome, email, telefone FROM tutores ORDER BY id"
    tutores = executar_sql(sql)
    return {
        "dados": [representar_tutor(tutor) for tutor in tutores],
        "didatica": {"sql": sql, "parametros": []},
    }

@app.get("/tutores/{tutor_id}")
def consultar_tutor(tutor_id: int = Path(gt=0)):
    sql = "SELECT id, nome, email, telefone FROM tutores WHERE id = %s"
    parametros = (tutor_id,)
    tutores = executar_sql(sql, parametros)

    if not tutores:
        raise HTTPException(status_code=404, detail="Tutor não encontrado")
    return {
        "dados": representar_tutor(tutores[0]),
        "didatica": {"sql": sql, "parametros": list(parametros)},
    }

@app.get("/pets")
def listar_pets(
    especie: str | None = Query(default=None, min_length=1, max_length=50),
):
    sql = SQL_PETS
    parametros = ()

    if especie is not None:
        sql += " WHERE p.especie = %s"
        parametros = (especie,)
    sql += " ORDER BY p.id"
    pets = executar_sql(sql, parametros)
    return {
        "dados": [representar_pet(pet) for pet in pets],
        "didatica": {"sql": sql, "parametros": list(parametros)},
    }

@app.get("/pets/{pet_id}")
def consultar_pet(pet_id: int = Path(gt=0)):
    sql = SQL_PETS + " WHERE p.id = %s"
    parametros = (pet_id,)
    pets = executar_sql(sql, parametros)

    if not pets:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return {
        "dados": representar_pet(pets[0]),
        "didatica": {"sql": sql, "parametros": list(parametros)},
    }