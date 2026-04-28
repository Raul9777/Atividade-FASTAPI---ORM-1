from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy .orm import Session
from database import SessionLocal
from .import models

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


# conexão com banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# HOME
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# =========================
# CATEGORIAS
# =========================

@app.get("/categorias")
def listar_categorias(request: Request, db: Session = Depends(get_db)):
    categorias = db.query(models.Categoria).all()
    return templates.TemplateResponse(
        "categorias.html",
        {"request": request, "categorias": categorias}
    )


@app.post("/categorias")
def criar_categoria(
    nome: str = Form(...),
    descricao: str = Form(None),
    db: Session = Depends(get_db)
):
    categoria = models.Categoria(nome=nome, descricao=descricao)
    db.add(categoria)
    db.commit()
    return {"msg": "Categoria criada"}


# =========================
# PRODUTOS
# =========================

@app.get("/produtos")
def listar_produtos(request: Request, db: Session = Depends(get_db)):
    produtos = db.query(models.Produto).all()
    categorias = db.query(models.Categoria).all()

    return templates.TemplateResponse(
        "produtos.html",
        {
            "request": request,
            "produtos": produtos,
            "categorias": categorias
        }
    )


@app.post("/produtos")
def criar_produto(
    nome: str = Form(...),
    preco: float = Form(...),
    estoque: int = Form(...),
    categoria_id: int = Form(...),
    db: Session = Depends(get_db)
):
    produto = models.Produto(
        nome=nome,
        preco=preco,
        estoque=estoque,
        categoria_id=categoria_id
    )

    db.add(produto)
    db.commit()
    return {"msg": "Produto criado"}