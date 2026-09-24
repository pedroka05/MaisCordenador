from typing import Annotated
from datetime import datetime

from fastapi import Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from main import app

# Models
### Student Model
class Aluno(SQLModel, table=True):
    id : int = Field(primary_key=True)
    Name : str = Field(index= True)
    age : int | None = None
    email : str 
    password : str

###
class Duvida(SQLModel, table=True):
    id : int = Field(primary_key= True)
    student_id : int = Field(foreign_key="aluno.id")
    date : datetime
    title : str
    text : str 
    resposta : str | None = None

### 
class Coodenador(SQLModel, table=True, ):
    id : int = Field(primary_key= True)
    id_duvida :int = Field(foreign_key="duvida.id")
    senha : str


#

mysql_bd_file = "database.mysql"
mysql_url = f"mysql:///{mysql_bd_file}"

connect_args = {"check_same_thread": False}
engine = create_engine(mysql_url, connect_args= connect_args)