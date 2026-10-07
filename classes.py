from typing import List, Optional
from sqlalchemy import String, Text, Integer, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Dublador(Base):
    __tablename__ = "tabela_dublador"
    
    # 4 Atributos: cpf, nome, idade, email
    cpf: Mapped[str] = mapped_column(String(11), primary_key=True)
    nome: Mapped[str] = mapped_column(String(250))
    idade: Mapped[int] = mapped_column(Integer)
    email: Mapped[str] = mapped_column(String(250))

    contratos: Mapped[List["Contrato"]] = relationship(
        back_populates="dublador", 
        cascade="all, delete-orphan"
    )


class Personagem(Base):
    __tablename__ = "tabela_personagem"
    
    # 4 Atributos: id, nome, producao_cinematografica, categoria
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(250))
    producao_cinematografica: Mapped[str] = mapped_column(Text)
    categoria: Mapped[str] = mapped_column(String(100))

    contratos: Mapped[List["Contrato"]] = relationship(
        back_populates="personagem", 
        cascade="all, delete-orphan"
    )


class Contrato(Base):
    __tablename__ = "tabela_contrato"

    # 4 Atributos: dublador_cpf, personagem_id, idioma, valor_cache
    dublador_cpf: Mapped[str] = mapped_column(
        String(11), 
        ForeignKey("tabela_dublador.cpf", ondelete="CASCADE"), 
        primary_key=True
    )
    personagem_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("tabela_personagem.id", ondelete="CASCADE"), 
        primary_key=True
    )
    idioma: Mapped[str] = mapped_column(String(50))
    valor_cache: Mapped[float] = mapped_column(Float)

    dublador: Mapped["Dublador"] = relationship(back_populates="contratos")
    personagem: Mapped["Personagem"] = relationship(back_populates="contratos")