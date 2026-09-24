from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

import functions as f

app = FastAPI()
templates = Jinja2Templates(directory="templates") ## Vai abrir o diretório 'Templates'

# Pagina Inicial
@app.get('/', include_in_schema= False)
def Homepage(request : Request):
    return templates.TemplateResponse(request,"index.html", {"title":"Home"}) ### Retorna o valor da variável "title"

@app.get('/login_aluno/', include_in_schema= False)
async def student_login(request: Request):
    return templates.TemplateResponse(request,"login_aluno.html")



@app.get('/login_coord/')
async def coord_login(request: Request):
    return templates.TemplateResponse(request,"login_coord.html")


@app.get('/login_coord/{coord_id}/painel')
async def coord(request: Request):
    return templates.TemplateResponse(request, "painel_coord.html")

