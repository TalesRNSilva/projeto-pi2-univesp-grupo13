from pydantic import BaseModel, model_validator, ConfigDict
from schema.base_schema import BaseSchema
import datetime as dt
from utils import convert_numeric_to_display_id

class ResponsavelResponse(BaseSchema):
    "Modelo de resposta da entidade Responsavel. Deve ser retornado em todo get que envolva a entidade."
    id: int
    nome: str
    email: str | None
    cadastro_timestamp: dt.datetime
    ativo: bool

    display_id:str = ""

    @model_validator(mode = 'after')
    def add_display_id(self):
        self.display_id = convert_numeric_to_display_id(self.id).replace('O', 'R')
        return self