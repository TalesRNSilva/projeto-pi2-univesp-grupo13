from datetime import datetime
from ..config import LOCAL_TZ
from pydantic import BaseModel, ConfigDict, model_validator

class BaseSchema(BaseModel):
    # Configuração moderna do Pydantic V2 para ler diretamente de objetos ORM (SQLModel)
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def converter_timezones_para_local(self) -> "BaseSchema":
        """Converte automaticamente qualquer datetime timezone-aware (geralmente UTC) 
        do banco para o fuso horário local em todas as respostas da API."""
        for field_name, value in self.__dict__.items():
            if isinstance(value, datetime) and value.tzinfo is not None:
                # Converte para o fuso local
                setattr(self, field_name, value.astimezone(LOCAL_TZ))
        return self