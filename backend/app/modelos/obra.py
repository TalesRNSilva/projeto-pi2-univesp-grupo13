from sqlmodel import Field, SQLModel, Relationship
from decimal import Decimal
from typing import Annotated
import datetime as dt
from ..config import LOCAL_TZ, StatusObra
from .responsavel import Responsavel

class Obra(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key = True) # O Id tá como opcional porque ele vai ser gerado pelo database. Então ele pode ser nulo no modelo
    projeto: str 
    data_inicio: dt.date
    data_conclusao: dt.date
    status: StatusObra = Field(default = 'Não iniciado')
    orcamento: Decimal | None = Field(default = None, max_digits = 10, decimal_places=2)
    endereco: str | None 
    descricao: str | None
    contratante: str | None
    telefone: str | None 
    email_contratante: str | None

    cadastro_timestamp: dt.datetime = Field(default_factory=lambda: dt.datetime.now(LOCAL_TZ))
    ultima_atualizacao: dt.datetime = Field(default_factory=lambda: dt.datetime.now(LOCAL_TZ))

    id_responsavel: int = Field(foreign_key = 'responsavel.id')
    responsavel: Responsavel = Relationship()
