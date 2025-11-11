from fastapi import FastAPI
from fastapi import Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DECIMAL

#DATABASE_URL = "postgresql://admin:JVoBXtBaUS2dQA0didZETSh8lonxCbBI@dpg-d496ttje5dus73cj2b1g-a/bdkayham"
DATABASE_URL = "postgresql://admin:JVoBXtBaUS2dQA0didZETSh8lonxCbBI@dpg-d496ttje5dus73cj2b1g-a.oregon-postgres.render.com/bdkayham"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, 
                            bind=engine)
Base = declarative_base()
# -------------------- Banco de Dados --------------------
# Modelo de tabela
class Livro(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), index=True)    
    preco = Column(DECIMAL(15, 2))
    disponibilidade = Column(Boolean)
    avaliacao = Column(DECIMAL(10))
    pagina = Column(DECIMAL(10))

# -------------------- FastAPI App --------------------
app = FastAPI(
    title="API de Consulta Livros",
    description="Serviço simples de consulta de livros",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "null"],  # Ou ["*"] para desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/livros")
def listar_livros(db=Depends(get_db)):
    # Modificação: Usar db.query(Livro).all() para retornar TODOS os campos de cada objeto Livro.
    livros = db.query(Livro).all()
    return livros
    
@app.get("/livros/search/{nome}")
def search_livros(nome: str, db=Depends(get_db)):
    """
    Busca livros por nome (título), usando uma pesquisa insensível a maiúsculas/minúsculas.
    """
    # Usamos .ilike() do SQLAlchemy para pesquisa case-insensitive com wildcards (%)
    # O % antes e depois permite buscar livros que CONTENHAM o termo.
    termo_pesquisa = f"%{nome.lower()}%"
    
    livros = db.query(Livro).filter(
        func.lower(Livro.titulo).like(termo_pesquisa)
    ).all()
    
    if not livros:
        raise HTTPException(status_code=404, detail=f"Nenhum livro encontrado com o nome '{nome}'")
        
    return livros

@app.get("/livros/{livro_id}") 
def get_livro(livro_id: int, db=Depends(get_db)): # O parâmetro agora é um inteiro
    livro = db.query(Livro).filter(Livro.id == livro_id).first() # Busca pelo ID
    if not livro:
        raise HTTPException(status_code=404, detail=f"Livro com ID {livro_id} não encontrado")
    return livro

#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=5001)