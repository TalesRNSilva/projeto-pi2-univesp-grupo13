# Arquivo para gerenciar a conexão com o DB e implementar funções utilitárias para administrar essa integração
# Ele não deve cuidar da atualização efetiva dos dados no db - isso fica para as funções à parte dentro desse mesmo módulo. 

from dotenv import load_dotenv
from pathlib import Path
import pymysql
import os
from tempfile import TemporaryDirectory

load_dotenv()

DB_HOST = os.getenv("DATABASE_HOST")
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_NAME = os.getenv("DATABASE_NAME")
CA_CERTIFICATE = os.getenv("CA_CERTIFICATE")

def get_connection():
    "Função que tenta criar uma conexão com o banco de dados MySQL usando as variáveis de ambiente definidas no arquivo .env."
    try:
        ca_file = build_ca_cert_file(CA_CERTIFICATE)
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
    finally:
        if conn:
            conn.close()