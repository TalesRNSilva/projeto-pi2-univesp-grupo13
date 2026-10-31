from datetime import date
from decimal import Decimal

from .db import get_session
from .modelos.obra import Obra
from .modelos.responsavel import Responsavel
from sqlmodel import select

dados_responsaveis_teste = [
    {'nome': 'Tales Silva', 'email': 'talesilva@teste.com'},
    {'nome': 'Francisco Chagas', 'email': 'franciscochagas@teste.com'},
    {'nome': 'Ludwig Wittgenstein', 'email': 'gramaticafilosofica@teste.com'},
]

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


def inserir_obras_teste():
    "Faz um upsert de 14 obras de teste."

    dados_obras_teste = [
        {'projeto': 'Reforma elétrica da casa', 'data_inicio': date(2026, 1, 5), 'data_conclusao': date(2026, 1, 20), 'status': 'Concluído', 'orcamento': Decimal('8500.00'), 'endereco': 'Rua das Palmeiras, 10', 'descricao': 'Substituição da rede elétrica antiga.', 'contratante': 'Ana Souza', 'telefone': '(11) 91234-1001', 'email_contratante': 'anasouza@teste.com', 'responsavel_email': 'talesilva@teste.com'},
        {'projeto': 'Instalação hidráulica da cozinha', 'data_inicio': date(2026, 2, 3), 'data_conclusao': date(2026, 2, 18), 'status': 'Em andamento', 'orcamento': Decimal('4200.50'), 'endereco': 'Av. Brasil, 200', 'descricao': None, 'contratante': 'Carlos Lima', 'telefone': '(11) 91234-1002', 'email_contratante': None, 'responsavel_email': 'franciscochagas@teste.com'},
        {'projeto': 'Construção de muro', 'data_inicio': date(2026, 2, 10), 'data_conclusao': date(2026, 3, 15), 'status': 'Em andamento', 'orcamento': Decimal('12300.00'), 'endereco': 'Rua do Comércio, 84', 'descricao': 'Muro com portão metálico.', 'contratante': 'Condomínio Vila Nova', 'telefone': None, 'email_contratante': 'vilanova@teste.com', 'responsavel_email': 'gramaticafilosofica@teste.com'},
        {'projeto': 'Pintura externa', 'data_inicio': date(2026, 3, 1), 'data_conclusao': date(2026, 3, 8), 'status': 'Concluído', 'orcamento': Decimal('2600.00'), 'endereco': 'Rua Serra Azul, 77', 'descricao': None, 'contratante': 'Marina Costa', 'telefone': '(11) 91234-1004', 'email_contratante': 'marina.costa@teste.com', 'responsavel_email': 'talesilva@teste.com'},
        {'projeto': 'Montagem de armários planejados', 'data_inicio': date(2026, 3, 12), 'data_conclusao': date(2026, 4, 5), 'status': 'Não iniciado', 'orcamento': Decimal('9800.00'), 'endereco': None, 'descricao': 'Armários para cozinha e suíte.', 'contratante': 'Paulo Vieira', 'telefone': '(11) 91234-1005', 'email_contratante': None, 'responsavel_email': 'franciscochagas@teste.com'},
        {'projeto': 'Reparo no telhado', 'data_inicio': date(2026, 4, 2), 'data_conclusao': date(2026, 4, 9), 'status': 'Encerrado', 'orcamento': Decimal('3100.75'), 'endereco': 'Estrada do Campo, 315', 'descricao': 'Obra interrompida por mudança de prazo.', 'contratante': None, 'telefone': None, 'email_contratante': 'telhado@teste.com', 'responsavel_email': 'gramaticafilosofica@teste.com'},
        {'projeto': 'Revestimento de banheiro', 'data_inicio': date(2026, 4, 14), 'data_conclusao': date(2026, 5, 2), 'status': 'Em andamento', 'orcamento': Decimal('6700.00'), 'endereco': 'Rua Central, 451', 'descricao': 'Troca de piso e revestimento.', 'contratante': 'João Prado', 'telefone': '(11) 91234-1007', 'email_contratante': 'joao.prado@teste.com', 'responsavel_email': 'talesilva@teste.com'},
        {'projeto': 'Instalação de portão automático', 'data_inicio': date(2026, 5, 5), 'data_conclusao': date(2026, 5, 12), 'status': 'Não iniciado', 'orcamento': None, 'endereco': 'Rua dos Ipês, 22', 'descricao': None, 'contratante': 'Beatriz Gomes', 'telefone': '(11) 91234-1008', 'email_contratante': None, 'responsavel_email': 'franciscochagas@teste.com'},
        {'projeto': 'Ampliação de varanda', 'data_inicio': date(2026, 5, 18), 'data_conclusao': date(2026, 7, 10), 'status': 'Em andamento', 'orcamento': Decimal('24900.00'), 'endereco': 'Av. das Flores, 890', 'descricao': 'Cobertura e piso em porcelanato.', 'contratante': 'Renato Alves', 'telefone': '(11) 91234-1009', 'email_contratante': 'renato.alves@teste.com', 'responsavel_email': 'gramaticafilosofica@teste.com'},
        {'projeto': 'Adequação de acessibilidade', 'data_inicio': date(2026, 6, 1), 'data_conclusao': date(2026, 6, 25), 'status': 'Concluído', 'orcamento': Decimal('18200.00'), 'endereco': 'Praça da Igreja, 5', 'descricao': 'Rampas e adaptações em sanitários.', 'contratante': 'Associação Santa Cruz', 'telefone': None, 'email_contratante': 'santacruz@teste.com', 'responsavel_email': 'talesilva@teste.com'},
        {'projeto': 'Troca de esquadrias', 'data_inicio': date(2026, 6, 15), 'data_conclusao': date(2026, 7, 1), 'status': 'Não iniciado', 'orcamento': Decimal('7400.00'), 'endereco': None, 'descricao': None, 'contratante': 'Fernanda Rocha', 'telefone': '(11) 91234-1011', 'email_contratante': None, 'responsavel_email': 'franciscochagas@teste.com'},
        {'projeto': 'Construção de área de lazer', 'data_inicio': date(2026, 7, 6), 'data_conclusao': date(2026, 9, 30), 'status': 'Em andamento', 'orcamento': Decimal('35650.00'), 'endereco': 'Rua do Lago, 18', 'descricao': 'Pergolado, piscina e área gourmet.', 'contratante': 'Lucas Mendes', 'telefone': '(11) 91234-1012', 'email_contratante': 'lucas.mendes@teste.com', 'responsavel_email': 'gramaticafilosofica@teste.com'},
        {'projeto': 'Impermeabilização de fachada', 'data_inicio': date(2026, 8, 3), 'data_conclusao': date(2026, 8, 21), 'status': 'Concluído', 'orcamento': None, 'endereco': 'Av. Paulista, 1400', 'descricao': 'Tratamento de fissuras e pintura.', 'contratante': 'Empresa Horizonte', 'telefone': '(11) 91234-1013', 'email_contratante': 'horizonte@teste.com', 'responsavel_email': 'talesilva@teste.com'},
        {'projeto': 'Reforma de escritório', 'data_inicio': date(2026, 9, 1), 'data_conclusao': date(2026, 10, 15), 'status': 'Não iniciado', 'orcamento': Decimal('21500.00'), 'endereco': 'Rua Augusta, 600', 'descricao': None, 'contratante': None, 'telefone': None, 'email_contratante': None, 'responsavel_email': 'franciscochagas@teste.com'},
    ]

    with get_session() as session:
        for obra in dados_obras_teste:
            responsavel_email = obra.pop('responsavel_email')
            data_to_insert = Obra(**obra)

            statement = select(Responsavel).where(Responsavel.email == responsavel_email)
            responsavel = session.exec(statement).one()
            data_to_insert.id_responsavel = responsavel.id

            statement = select(Obra).where(Obra.projeto == data_to_insert.projeto)
            existing_data = session.exec(statement).first()

            if existing_data:
                for field_name, value in obra.items():
                    setattr(existing_data, field_name, value)
                existing_data.id_responsavel = responsavel.id
                session.add(existing_data)
            else:
                session.add(data_to_insert)
        session.commit()

        statement = select(Obra).where(Obra.email_contratante.like("%@teste.com"))
        results = session.exec(statement)
        for data in results:
            print(data)


def inserir_dados_teste():
    "Insere os dados de responsáveis e obras marcados para teste."

    inserir_responsaveis_teste()
    inserir_obras_teste()


def remover_dados_teste():
    "Remove as obras e responsáveis marcados para teste."

    with get_session() as session:
        ids_responsaveis_teste = select(Responsavel.id).where(
            Responsavel.email.like("%@teste.com")
        )
        obras_teste = session.exec(
            select(Obra).where(Obra.id_responsavel.in_(ids_responsaveis_teste))
        ).all()
        for obra in obras_teste:
            session.delete(obra)

        responsaveis_teste = session.exec(
            select(Responsavel).where(Responsavel.email.like("%@teste.com"))
        ).all()
        for responsavel in responsaveis_teste:
            session.delete(responsavel)
        session.commit()
