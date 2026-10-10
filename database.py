from typing import Annotated
from datetime import datetime

from fastapi import Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


# Models
### Student Model
class Aluno(SQLModel, table=True):
    id : int = Field(primary_key=True)
    Name : str = Field(index= True)
    id_Turma : int = Field(foreign_key= "turma.id")
    age : int | None = None
    email : str 
    password : str

class Turma(SQLModel, table = True):
    id : int = Field(primary_key=True)
    nome : str


### 
class Coodenador(SQLModel, table=True, ):
    id : int = Field(primary_key= True)
    id_duvida :int = Field(foreign_key="duvida.id")
    id_turma : int = Field(foreign_key="turma.id")
    senha : str

class Duvida(SQLModel, table=True):
    id : int = Field(primary_key= True)
    student_id : int = Field(foreign_key="aluno.id")
    date : datetime
    title : str
    text : str 
    resposta : str | None = None

#

sql_bd_file = "database.bd"
sql_url = f"sqlite:///{sql_bd_file}"

connect_args = {"check_same_thread": False}
engine = create_engine(sql_url, connect_args= connect_args)

def create_db_and_tables():
    return SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine):
        yield session

Sessiondep = Annotated[Session, Depends(get_session)]