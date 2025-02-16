from sqlmodel import SQLModel, Field, create_engine;
from enum import Enum;
from datetime import date;  

# CRIAÇÃO DO BANCO 
class Bancos(Enum):
  NUBANK = "Nubank";
  ITAU = "Itaú";
  BRADESCO = "Bradesco";
  SANTANDER = "Santander";
  INTER = "Inter";


class Status(Enum):
  ATIVO = 'Ativo';
  INATIVO = 'Inativo';
 # C

class Conta(SQLModel, table=True): # Classe que representa a tabela Conta
  id: int = Field(primary_key=True); # Campo id é a chave primária
  banco: Bancos = Field(default=Bancos.NUBANK); #Se o usuário não informou o banco, o padrão é Nubank
  status: Status = Field(default=Status.ATIVO);
  valor: float;
 

# MOVIMENTAÇÃO FINANCEIRA

class Tipos(Enum): # Enum que representa os tipos de movimentação financeira
  ENTRADA = 'Entrada';
  SAIDA = 'Saída';

class Historico(SQLModel, table=True): # Classe que representa a tabela Histórico
  id: int = Field(primary_key=True); # Campo id é a chave primária
  conta_id: int = Field(foreign_key="conta.id"); # Chave estrangeira para a tabela Conta
  conta: Conta = Relationship() # Relacionamento com a tabela Conta  
  tipo: Tipos = Field(default=Tipos.ENTRADA); # Tipo da movimentação financeira
  valor: float; # Valor da movimentação financeira
  data: date; # Data da movimentação financeira


sqlite_file_name = 'database.db'; # Nome do arquivo de banco de dados
sqlite_url = f"sqlite:///{sqlite_file_name}"; # URL de conexão com o banco de dados 

engine = create_engine(sqlite_url, echo=True); # Cria a engine de conexão com o banco de dados

if __name__ == "__main__":
  SQLModel.metadata.create_all(engine); # Cria as tabelas no banco de dados

#para rodar o código: python3 models.py

