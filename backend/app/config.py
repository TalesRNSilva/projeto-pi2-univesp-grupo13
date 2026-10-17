# Aqui são configurações compartilhadas entre os módulos do back-end
# Coisas como ENUMs, opções de conexão, e afins
# Esse arquivo não precisa necessariamente estar preenchido, mas
# parâmetros comuns a todos os módulos devem vir aqui

import datetime as dt
from zoneinfo import ZoneInfo
from enum import Enum

LOCAL_TZ = ZoneInfo('America/Sao_Paulo')

class StatusObra(str, Enum):
    NAO_INICIADO = "Não iniciado"
    EM_ANDAMENTO = 'Em andamento'
    CONCLUIDO = "Concluído"
    ENCERRADO = "Encerrado" # A diferença dos dois é que encerrado é quando a obra foi abandonada antes de sua conclusão

if __name__ == "__main__":
    print(dt.datetime.now(tz = LOCAL_TZ)) # Verificando TZ Local