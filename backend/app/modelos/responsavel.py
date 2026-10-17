from sqlmodel import Field, SQLModel
from typing import Annotated
import datetime as dt
from config import LOCAL_TZ

class Responsavel(SQLModel, table = True):
    id: int | None = Field(primary_key = True) # O Id tá como opcional porque ele vai ser gerado pelo database. Então ele pode ser nulo no modelo
    nome: str
    email: str | None
    ativo: bool = Field(default = True)
    cadastro_timestamp: dt.datetime = Field(default_factory = lambda: dt.datetime.now(LOCAL_TZ))