from models import Conta, Status, engine, Bancos, Tipos, Historico;
from sqlmodel import Session, select;
from datetime import date;

# MANIPULAÇÃO DA CONTA
def criar_conta(conta: Conta):
  with Session(engine) as session:                    # gerenciador de contexto
    statement = select(Conta).where(Conta.banco == conta.banco); # Cria a query de seleção
    results = session.exec(statement).all();          # Executa a query e pega todos os resultados
    if results:                                       # Se já existe uma conta nesse banco
      print("Já existe uma conta nesse banco ");
      return None; 

    session.add(conta);                               # Adiciona a conta no banco de dados
    session.commit();                                 # Salva a conta no banco de dados
    return conta;


def listar_contas(): 
  with Session(engine) as session:                    # Isso garante que a sessão será fechada automaticamente ao final da execução
    statement = select(Conta)                         # É equivalente ao SQL: "SELECT * FROM conta"
    results = session.exec(statement).all()           # Executa a consulta no banco de dados e retorna todos os resultados
    return results;

def desativar_conta(id): 
  with Session(engine) as session:
    statement = select(Conta).where(Conta.id==id);    # Busca a conta com o ID fornecido
    conta = session.exec(statement).first()           # Obtém o primeiro resultado da busca   
    if conta.valor > 0:                               # Se conta tem saldo           
      raise ValueError('Essa conta ainda possui saldo, não é possível desativar.')        
    
    conta.status = Status.INATIVO                     # Se não, conta desativada      
    session.commit()

def transferir_saldo(id_conta_saida, id_conta_entrada, valor):
  with Session(engine) as session:                      
    statement = select(Conta).where(Conta.id==id_conta_saida)        
    conta_saida = session.exec(statement).first()     # Conta da onde o dinheiro vai sair

    if conta_saida.valor < valor:                     # Se o valor da conta for menor do que o usuário quer transferir
     raise ValueError('Saldo insuficiente')    
        
    statement = select(Conta).where(Conta.id==id_conta_entrada) # Conta onde vai entrar o dinheiro       
    conta_entrada = session.exec(statement).first()                  

  # taxa
  # taxa = valor * 1 / 100
  # conta_entrada.valor += (valor - taxa)

  conta_saida.valor -= valor        
  conta_entrada.valor += valor        
  session.commit()

def movimentar_dinheiro(historico: Historico): # Função para movimentar dinheiro
  with Session(engine) as session:
    statement = select(Conta).where(Conta.id == historico.conta_id);
    conta = session.exec(statement).first();

    #TODO: Validar se a conta está ativa
    if conta.status == Status.INATIVO:
      raise ValueError("Conta inativa");
  
    if historico.tipo == Tipos.ENTRADA:
      conta.valor += historico.valor
    else:
      if conta.valor < historico.valor:
        raise ValueError("Saldo insuficiente")
      conta.valor -= historico.valor

    session.add(historico)                             # Adiciona o histórico no banco de dados
    session.commit()                                   # Salva o histórico no banco de dados
    return historico;

def total_contas():                                   # Função para calcular o total de todas as contas
  with Session(engine) as session:
    statement = select(Conta)
    contas = session.exec(statement).all()            # Pega todas as contas
    total = 0                                         # Inicializa o total como 0
    for conta in contas:                              # Para cada conta
      total += conta.valor                            # Adiciona o valor da conta ao total
    return float(total);  

# ANÁLISE DE DADOS
def buscar_historicos_entre_datas(data_inicial: date, data_fim: date): # Função para buscar históricos entre duas datas
  with Session(engine) as session:
    statement = select(Historico).where
    (Historico.data >= data_inicial).where
    (Historico.data <= data_fim);
  resultados = session.exec(statement).all();
  return resultados

# Gráfico
import matplotlib.pyplot as plt;

#plt.bar(['NUBANK', 'SANTANDER'], [10, 5])
#plt.show();

# def criar_grafico_por_conta():
#   with Session(engine) as session:
#     statement = select(Conta).where(Conta.status == Status.ATIVO);
#     contas = session.exec(statement).all()
#     bancos = []
# for i in contas;
#   bancos.append(i.banco.value)
#   print(bancos)
# faria o mesmo para total
#  total = []
# for i in contas:
#...

def criar_grafico_por_conta():
  with Session(engine) as session:
    statement = select(Conta).where(Conta.status == Status.ATIVO);
    contas = session.exec(statement).all()
    bancos = [i.banco.value for i in contas]
    total = [i.valor for i in contas]

    plt.bar(bancos, total)
    plt.show()

# criar_grafico_por_conta()

                                                      # Teste de criação de conta
# conta = Conta(valor=0, banco=Bancos.INTER);         # Cria uma conta
# criar_conta(conta);

# desativar_conta(1);

# transferir_saldo(5, 1);

# historico = Historico(conta_id=1, tipo=Tipos.ENTRADA, valor=10, data=date.today());
# movimentar_dinheiro(historico);

#print(total_contas());                               # Imprime o total de todas as contas

# x = buscar_historicos_entre_datas(date.today() - timedelta(days=1), date.today() + timedelta(days=1)); # Busca históricos entre ontem e amanhã
#print(x);