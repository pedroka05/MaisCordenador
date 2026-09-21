from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

import functions as f

app = FastAPI()
templates = Jinja2Templates(directory="templates") ## Vai abrir o diretório 'Templates'

# Pagina Inicial
@app.get('/', include_in_schema= False)
def Homepage(request : Request):
    return templates.TemplateResponse(request,"index.html", {"title":"Home"}) ### Retorna o valor da variável "title"

