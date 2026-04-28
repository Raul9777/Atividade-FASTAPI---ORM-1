from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, database

app = FastAPI()

# Aponta para a pasta de templates dentro de app
templates = Jinja2Templates(directory="app/templates")

# Cria as tabelas ao iniciar 
models.Base.metadata.create_all(bind=database.engine)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/categorias", response_class=HTMLResponse)
def listar_categorias(request: Request, db: Session = Depends(database.get_db)):
    categorias = db.query(models.Categoria).all()
    return templates.TemplateResponse("categorias.html", {"request": request, "categorias": categorias})

@app.get("/produtos", response_class=HTMLResponse)
def listar_produtos(request: Request, db: Session = Depends(database.get_db)):
    produtos = db.query(models.Produto).all()
    categorias = db.query(models.Categoria).all()
    return templates.TemplateResponse("produtos.html", {
        "request": request, 
        "produtos": produtos,
        "categorias": categorias
    })

@app.post("/produtos/novo")
def criar_produto(
    nome: str = Form(...), 
    preco: float = Form(...), 
    estoque: int = Form(...), 
    categoria_id: int = Form(...), 
    db: Session = Depends(database.get_db)
):
    novo_p = models.Produto(nome=nome, preco=preco, estoque=estoque, categoria_id=categoria_id)
    db.add(novo_p)
    db.commit()
    return RedirectResponse(url="/produtos", status_code=303)


@app.post("/categorias/nova")
def criar_categoria(nome: str = Form(...), descricao: str = Form(None), db: Session = Depends(database.get_db)):
    nova_cat = models.Categoria(nome=nome, descricao=descricao)
    db.add(nova_cat)
    db.commit()
    return RedirectResponse(url="/categorias", status_code=303)