from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, database

app = FastAPI(title="Sistema de Loja 1:N")

# Certifique-se de que a pasta 'templates' está dentro da pasta 'app'
templates = Jinja2Templates(directory="app/templates")

# Cria as tabelas no banco de dados (banco.db)
models.Base.metadata.create_all(bind=database.engine)

# --- ROTAS DE CATEGORIAS ---

@app.get("/categorias", response_class=HTMLResponse)
def listar_categorias(request: Request, db: Session = Depends(database.get_db)):
    # O .all() é fundamental para converter a query em uma lista
    categorias = db.query(models.Categoria).all()
    return templates.TemplateResponse("categorias.html", {"request": request, "categorias": categorias})

@app.post("/categorias/nova")
def criar_categoria(
    nome: str = Form(...), 
    descricao: str = Form(None), 
    db: Session = Depends(database.get_db)
):
    nova_cat = models.Categoria(nome=nome, descricao=descricao)
    db.add(nova_cat)
    db.commit()
    return RedirectResponse(url="/categorias", status_code=303)

# --- ROTAS DE PRODUTOS ---

@app.get("/produtos", response_class=HTMLResponse)
def listar_produtos(request: Request, db: Session = Depends(database.get_db)):
    produtos = db.query(models.Produto).all()
    categorias = db.query(models.Categoria).all() # Necessário para o formulário de cadastro
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
    novo_p = models.Produto(
        nome=nome, 
        preco=preco, 
        estoque=estoque, 
        categoria_id=categoria_id
    )
    db.add(novo_p)
    db.commit()
    return RedirectResponse(url="/produtos", status_code=303)

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})