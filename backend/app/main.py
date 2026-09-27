### Módulo que vai gerenciar as rotas e instanciar o APP
from db.db_conn import *

if __name__ == "__main__":
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 AS connected")
        print(cursor.fetchone())
