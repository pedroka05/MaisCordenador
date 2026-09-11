from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="dist")

# Pagina Inicial
@app.get('/')
def Homepage(request : Request):
    return templates.TemplateResponse(request = request, name="index.html")

@app.get('/tirarduvida/')
def askprincipal():
    return {"message": "Hello World"}