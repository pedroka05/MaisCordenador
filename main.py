from fastapi import FastAPI, Request,responses,Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated

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

@app.get('/login_aluno/', name= "student_login",include_in_schema= False)
async def student_login(request: Request):
    return templates.TemplateResponse(request,"login_aluno.html")

@app.post('/login_aluno', name='form_login_aluno')
async def student_login_form(request: Request, session: db.Sessiondep, id: Annotated[int, Form(alias="id")], password: Annotated[str, Form(alias="password")]):
    ### Fazer ele retornar o valor ta dando certo, so que tem que por algumas mudanças tipo senha ser feita em hashes
    # O msm vale para "coord_login"
    if id == db.ALUNO_FANTASMA["id"] and password == db.ALUNO_FANTASMA["password"]:
        return responses.RedirectResponse(url="/painel_aluno", status_code= 303)

@app.get('/login_coord/')
async def coord_login(request: Request, id: Annotated[int, Form(alias="id")], password: Annotated[str, Form(alias="password")]):
    return templates.TemplateResponse(request,"login_coord.html")


@app.get('/login_coord/{coord_id}/painel')
async def coord(request: Request):
    return templates.TemplateResponse(request, "painel_coord.html")


@app.get("/painel_aluno", name="painel_aluno", include_in_schema=False)
def painel_aluno(request:Request):
    return templates.TemplateResponse(request, "painel_aluno.html")