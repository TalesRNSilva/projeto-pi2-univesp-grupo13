from db import get_session
from modelos.responsavel import Responsavel
from sqlmodel import select

dados_responsaveis_teste = [{'nome': 'Tales Silva', 'email' : 'talesilva@teste.com'},
    {'nome': 'Francisco Chagas', 'email' : 'franciscochagas@teste.com'},
    {'nome': 'Ludwig Wittgenstein', 'email' : 'gramaticafilosofica@teste.com'}]

def inserir_responsaveis_teste():
    "Faz um upsert de dados de responsáveis para teste."

    with get_session() as session:
        for responsavel in dados_responsaveis_teste:
            data_to_insert = Responsavel(**responsavel)

            statement = select(Responsavel).where(Responsavel.email == data_to_insert.email)
            existing_data = session.exec(statement).first()

            if existing_data:
                existing_data.nome = data_to_insert.nome 
                existing_data.ativo = data_to_insert.ativo
                session.add(existing_data)
            else:
                session.add(data_to_insert)
        session.commit()

        statement = select(Responsavel).where(Responsavel.email.like("%@teste.com"))
        results = session.exec(statement)
        for data in results:
            print(data)



