from typing import Annotated
from datetime import datetime,timezone

from fastapi import Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select,Relationship


# Models
class Turma(SQLModel, table = True):
    id : int = Field(primary_key=True)
    nome : str

    alunos: list["Aluno"] = Relationship(back_populates="turma")
    coordenadores: list["Coordenador"] = Relationship(back_populates="turmas", link_model="CoordendorTurma")

class Aluno(SQLModel, table=True):
    id : int = Field(primary_key=True)
    username : str = Field(index= True)
    id_Turma : int = Field(foreign_key= "turma.id")
    age : int | None = None
    email : str
    password : str

    turma: Turma = Relationship(back_populates="alunos")
    duvidas: list["Duvida"] = Relationship(back_populates="aluno") 


class Coodenador(SQLModel, table=True, ):
    id : int = Field(primary_key= True)
    username : str = Field(index= True)
    id_duvida :int = Field(foreign_key="duvida.id")
    id_turma : int = Field(foreign_key="turma.id")
    senha : str

class CoordenadorTurma(SQLModel, table=True):  # tabela intermediária (N:N)
    coordenador_id: int = Field(foreign_key="coordenador.id", primary_key=True)
    turma_id: int = Field(foreign_key="turma.id", primary_key=True)

class Duvida(SQLModel, table=True):
    id : int = Field(primary_key= True)
    student_id : int = Field(foreign_key="aluno.id")
    date : datetime.now(timezone.utc)
    title : str
    text : str
    status : str| Field(default="aberta")

    aluno: Aluno = Relationship(back_populates="duvidas")
    respostas: list["Resposta"] = Relationship(back_populates="duvida")

class Resposta(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    duvida_id: int = Field(foreign_key="duvida.id")
    coordenador_id: int = Field(foreign_key="coordenador.id")
    texto: str
    criada_em: datetime = Field(default_factory=datetime.now(timezone.utc))

    duvida: Duvida = Relationship(back_populates="respostas")
    coordenador: Coordenador = Relationship(back_populates="respostas")


sql_bd_file = "database.bd"
sql_url = f"sqlite:///{sql_bd_file}"

connect_args = {"check_same_thread": False}
engine = create_engine(sql_url, connect_args= connect_args)

def create_db_and_tables():
    return SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

Sessiondep = Annotated[Session, Depends(get_session)]
