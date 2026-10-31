from pydantic import BaseModel, model_validator, ConfigDict, computed_field
from typing import List
from .base_schema import BaseSchema
from .responsavel import ResponsavelResponseLean
from decimal import Decimal
from sqlmodel import Field
import datetime as dt
from ..config import StatusObra
from ..utils import convert_numeric_to_display_id

class ObraResponse(BaseSchema):
    id: int = Field(exclude = True)
    projeto: str 
    data_inicio: dt.date
    data_conclusao: dt.date
    status: StatusObra
    orcamento: Decimal | None = Field(default = None, max_digits = 10, decimal_places=2)
    endereco: str | None 
    descricao: str | None
    contratante: str | None
    telefone: str | None 
    email_contratante: str | None
    id_responsavel: int

    cadastro_timestamp: dt.datetime
    ultima_atualizacao: dt.datetime

    responsavel: ResponsavelResponseLean

    @computed_field
    @property
    def display_id(self) -> str:
        return convert_numeric_to_display_id(self.id)


class ObrasPaginatedResponse(BaseSchema):
    obras: List[ObraResponse]
    current_page: int
    total_pages: int
    total_items: int


class ObraPost(BaseSchema):
    projeto: str 
    data_inicio: dt.date
    data_conclusao: dt.date
    status: StatusObra
    orcamento: Decimal | None = Field(default = None, max_digits = 10, decimal_places=2)
    endereco: str | None = None
    descricao: str | None = None
    contratante: str | None = None
    telefone: str | None  = None
    email_contratante: str | None = None

    id_responsavel : int

class ObraPut(BaseSchema):
    projeto: str | None = None
    data_inicio: dt.date | None = None
    data_conclusao: dt.date | None = None
    status: StatusObra | None = None
    orcamento: Decimal | None = Field(default = None, max_digits = 10, decimal_places=2)
    endereco: str | None = None
    descricao: str | None = None
    contratante: str | None = None
    telefone: str | None  = None
    email_contratante: str | None = None

    id_responsavel : int | None = None