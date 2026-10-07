import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from classes import Base, Dublador, Personagem, Contrato

load_dotenv()

# Variáveis globais para gestão de conexão
engine = None
banco_atual = "Nenhum"

def conectar_banco(opcao: int) -> bool:
    global engine, banco_atual
    try:
        if opcao == 1:
            engine = create_engine("sqlite:///banco.db", echo=False)
            banco_atual = "SQLite (banco.db)"
        elif opcao == 2:
            host = os.getenv("DB_HOST")
            user = os.getenv("DB_USER")
            password = os.getenv("DB_PASS")
            port = os.getenv("DB_PORT")
            dbname = os.getenv("DB_NAME", "defaultdb")

            url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
            engine = create_engine(url, echo=False)
            banco_atual = f"MySQL ({host})"
        else:
            print("Opção de conexão inválida.")
            return False

        Base.metadata.create_all(engine)
        print(f"\nConectado com sucesso a: {banco_atual}")
        return True
    except Exception as e:
        print(f"\nErro ao conectar à base de dados: {e}")
        return False


# --- OPERAÇÕES DE INSERÇÃO ---

def adicionar_dublador():
    if not engine:
        print("Conecte-se a uma base de dados primeiro!")
        return

    dcpf = input("Informe o CPF (apenas números): ")
    dnome = input("Informe o Nome: ")
    didade = int(input("Informe a idade: "))
    demail = input("Informe o Email: ")

    with Session(engine) as session:
        try:
            dublador = Dublador(cpf=dcpf, nome=dnome, idade=didade, email=demail)
            session.add(dublador)
            session.commit()
            print("Dublador inserido com sucesso!")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao inserir dublador: {e}")


def adicionar_personagem():
    if not engine:
        print("Conecte-se a uma base de dados primeiro!")
        return

    pnome = input("Informe o nome do personagem: ")
    pproducao = input("Informe a produção cinematográfica: ")
    pcategoria = input("Informe a categoria (ex: Principal, Secundário): ")

    with Session(engine) as session:
        try:
            personagem = Personagem(
                nome=pnome, 
                producao_cinematografica=pproducao, 
                categoria=pcategoria
            )
            session.add(personagem)
            session.commit()
            print("Personagem inserido com sucesso!")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao inserir personagem: {e}")


def relacionar_dublador_personagem():
    if not engine:
        print("Conecte-se a uma base de dados primeiro!")
        return

    dublador_cpf = input("Insira o CPF do dublador: ")
    personagem_id = int(input("Insira o ID do personagem: "))
    contrato_idioma = input("Informe o idioma do contrato: ")
    valor_cache = float(input("Informe o valor do cachê: "))

    with Session(engine) as session:
        try:
            dub = session.scalar(select(Dublador).where(Dublador.cpf == dublador_cpf))
            pers = session.scalar(select(Personagem).where(Personagem.id == personagem_id))

            if not dub or not pers:
                print("Erro: Dublador ou Personagem não encontrado.")
                return

            contrato = Contrato(
                dublador=dub,
                personagem=pers,
                idioma=contrato_idioma,
                valor_cache=valor_cache
            )
            session.add(contrato)
            session.commit()
            print("Contrato registado com sucesso!")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao registar contrato: {e}")


# --- OPERAÇÕES DE LISTAGEM ---

def listar_dubladores():
    if not engine: return
    with Session(engine) as session:
        dubladores = session.scalars(select(Dublador)).all()
        print("\n--- Dubladores Registo ---")
        for d in dubladores:
            print(f"CPF: {d.cpf} | Nome: {d.nome} | Idade: {d.idade} | Email: {d.email}")


def listar_personagens():
    if not engine: return
    with Session(engine) as session:
        personagens = session.scalars(select(Personagem)).all()
        print("\n--- Personagens Registo ---")
        for p in personagens:
            print(f"ID: {p.id} | Nome: {p.nome} | Produção: {p.producao_cinematografica} | Categoria: {p.categoria}")


def listar_contratos():
    if not engine: return
    with Session(engine) as session:
        contratos = session.scalars(select(Contrato)).all()
        print("\n--- Contratos Registados ---")
        for c in contratos:
            print(f"Dublador: {c.dublador.nome} ({c.dublador_cpf}) | "
                  f"Personagem: {c.personagem.nome} (ID: {c.personagem_id}) | "
                  f"Idioma: {c.idioma} | Cachê: R${c.valor_cache:.2f}")


# --- OPERAÇÕES DE EXCLUSÃO ---

def excluir_dublador():
    if not engine: return
    cpf = input("Informe o CPF do dublador a excluir: ")
    with Session(engine) as session:
        try:
            dub = session.scalar(select(Dublador).where(Dublador.cpf == cpf))
            if dub:
                session.delete(dub)
                session.commit()
                print("Dublador (e os seus contratos) eliminado com sucesso!")
            else:
                print("Dublador não encontrado.")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao eliminar: {e}")


def excluir_personagem():
    if not engine: return
    p_id = int(input("Informe o ID do personagem a excluir: "))
    with Session(engine) as session:
        try:
            pers = session.scalar(select(Personagem).where(Personagem.id == p_id))
            if pers:
                session.delete(pers)
                session.commit()
                print("Personagem (e os seus contratos) eliminado com sucesso!")
            else:
                print("Personagem não encontrado.")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao eliminar: {e}")


def excluir_contrato():
    if not engine: return
    cpf = input("Informe o CPF do dublador no contrato: ")
    p_id = int(input("Informe o ID do personagem no contrato: "))
    with Session(engine) as session:
        try:
            contrato = session.scalar(
                select(Contrato).where(
                    Contrato.dublador_cpf == cpf, 
                    Contrato.personagem_id == p_id
                )
            )
            if contrato:
                session.delete(contrato)
                session.commit()
                print("Contrato eliminado com sucesso!")
            else:
                print("Contrato não encontrado.")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao eliminar contrato: {e}")