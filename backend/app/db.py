# Arquivo para gerenciar a conexão com o DB e implementar funções utilitárias para administrar essa integração
# Ele não deve cuidar da atualização efetiva dos dados no db - isso fica para as funções à parte dentro desse mesmo módulo. 

from dotenv import load_dotenv
from pathlib import Path
import pymysql
import os
from tempfile import TemporaryDirectory
from sqlalchemy import URL, Engine
from sqlmodel import create_engine, Session
from collections.abc import Generator

load_dotenv()

DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_NAME = os.getenv("DATABASE_NAME")
CA_CERTIFICATE = os.getenv("CA_CERTIFICATE")
DB_SSL_CA = os.getenv("DATABASE_SSL_CA")
ECHO = True

def get_connection():
    "Função que tenta criar uma conexão com o banco de dados MySQL usando as variáveis de ambiente definidas no arquivo .env."
    try:
        ca_file = get_ca_pem_path()
        conn = pymysql.connect(
            host = DB_HOST,
            database = DB_NAME,
            port = 11838,
            user = DB_USER,
            password = DB_PASSWORD,
            charset = "utf8mb4",
            connect_timeout = 10,
            cursorclass = pymysql.cursors.DictCursor,
            ssl = {"ca": ca_file} if ca_file else None,
            read_timeout = 10
        )
        return conn
    except:
        raise

def build_ca_cert_file(ca_certificate = CA_CERTIFICATE) -> str:
    "Essa função cria um arquivo temporário com o certificado CA, caso seja necessário, e retorna o caminho para esse arquivo."
    with TemporaryDirectory() as temporary_directory:
        if "-----BEGIN CERTIFICATE-----" in ca_certificate:
            ca_path = Path(temporary_directory) / "aiven-ca.pem"
            ca_path.write_text(ca_certificate.replace("\\n", "\n"), encoding="ascii")
            ca_file = str(ca_path)
        elif Path(ca_certificate).is_file():
            ca_file = ca_certificate
            return ca_file
        else:
            raise FileNotFoundError(
                "CA_CERTIFICATE must point to a CA file or contain PEM certificate text")

def test_db_connection():
    "Função para testar a conexão com o banco de dados."
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 AS connected")
            print(cursor.fetchone())
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_db_url():
    "Função para facilitar criação de URI de conexão. Só deve ser usada internamente: nunca printar."
    # uri = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    url = URL.create(
        drivername = 'mysql+pymysql',
        username = DB_USER,
        password = DB_PASSWORD,
        port = DB_PORT,
        database = DB_NAME,
        host = DB_HOST
    )
    return url

def get_ca_pem_path():
    "Função utilitária para puxar o path do ca.pem"
    cwd = Path.cwd()
    path_string = str(cwd)
    current_directory = path_string.split('\\')[-1]
    if current_directory == 'app':
        ca_pem_path = cwd.parent / DB_SSL_CA
    elif current_directory == 'backend':
        ca_pem_path = cwd / DB_SSL_CA
    elif current_directory == 'projeto-pi2-univesp-grupo13':
        ca_pem_path = cwd / 'backend' / DB_SSL_CA
    else:
        raise ValueError('Unkown Directory')
    return str(ca_pem_path)

def get_sql_engine(echo = ECHO) -> Engine:
    "Função para retornar uma engine de SQLAlchemy pronta pra rodar."
    url = get_db_url()
    connect_args = {
        'ssl' : {
                'ca' : get_ca_pem_path()
            }
        }
    engine = create_engine(url = url, connect_args=connect_args, echo = echo)
    return engine

engine = get_sql_engine()

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session