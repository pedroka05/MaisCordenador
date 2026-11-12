from fastapi import FastAPI, Request,responses,Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from starlette.middleware.sessions import SessionMiddleware

from typing import Annotated
from pathlib import Path

import database as db

app = FastAPI()
templates = Jinja2Templates(directory="templates") ## Vai abrir o diretório 'Templates'
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def on_startup():
    db.create_db_and_tables()


# Pagina Inicial
@app.get('/', include_in_schema= False)
def Homepage(request : Request):
    return templates.TemplateResponse(request,"index.html", {"title":"Home"}) ### Retorna o valor da variável "title"


# ALUNOS

### Autenticação do Aluno
@app.get('/login_aluno/', name= "student_login",include_in_schema= False)
async def student_login(request: Request):
    return templates.TemplateResponse(request,"login_aluno.html")

@app.post('/login_aluno/', name='form_login_aluno') ## This could not be the best way to make a authentication but i will use it as a "quebra galho"
async def student_login_form(request: Request, session: db.Sessiondep, id: Annotated[int, Form(alias="id")], password: Annotated[str, Form(alias="password")]):

    aluno = session.get(db.Aluno, id)

    if aluno is None or aluno.password != password:
        raise HTTPException(status_code=401, detail="ID ou senha incorretos")

    return responses.RedirectResponse(url=f"/{aluno.id}/painel_aluno", status_code= 303,)


### Painel do Aluno
@app.get("/{aluno_id}/painel_aluno", name="painel_aluno", include_in_schema=False)
def painel_aluno(request:Request, aluno_id: int):
    return templates.TemplateResponse(request, "painel_aluno.html", {"aluno_id": aluno_id})


### DÚVIDAS
@app.get("/{aluno_id}/painel_aluno/duvidas", name = "duvidas_aluno", include_in_schema=False) # Isso em teoria vai funcionar Também
async def Duvidas(request:Request, session: db.Sessiondep):
    return templates.TemplateResponse(request,"duvidas_aluno.html")

@app.get("/{aluno_id}/painel_aluno/duvidas", name="duvidas_aluno")
async def List_Duvidas(aluno_id: int, request: Request, session: db.Sessiondep):
    duvidas = session.exec(
        select(db.Duvida).where(db.Duvida.student_id == aluno_id)
    ).all()

    return templates.TemplateResponse(
        request,
        "duvidas_aluno.html",
        {"aluno_id": aluno_id, "duvidas": duvidas},
    )

@app.post("/{aluno_id}/painel_aluno/duvidas") ## Na teoria isso funciona, tem que ver na pratica dps
async def Create_Duvida(aluno_id: int,session: db.Sessiondep, title:Annotated[str, Form(alias="title")], body: Annotated[str, Form(alias="bodytext")]):

    duvida = db.Duvida(student_id=aluno_id, title= title, text= body)

    session.add(duvida)
    session.commit
    session.refresh(duvida)

    return duvida




# COORDENADOR

@app.get('/login_coord/', name="principal_login", include_in_schema= False)
async def coord_login(request: Request):
    return templates.TemplateResponse(request,"login_coord.html")

@app.post('/login_coord/')
async def coord_login_form( session: db.Sessiondep, id: Annotated[int, Form(alias="id")], password: Annotated[str, Form(alias="password")]):

    coord = session.get(db.Coordenador, id)

    if coord is None or coord.senha != password:
        raise HTTPException(status_code=401, detail="ID ou senha incorretos")

    return responses.RedirectResponse(url=f"/{coord.id}/painel_coord", status_code= 303,)


### Painel do Coordenador
@app.get('/{coord_id}/painel_coord', include_in_schema=False, name="painel_coord")
async def coord(request: Request): 
    return templates.TemplateResponse(request, "painel_coord.html")
