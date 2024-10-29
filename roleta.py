import numpy as np;
import plotly.express as px;
import pandas as pd;

## Classe dos jogadores
class Jogador:
    def __init__(self, dinheiro):
        self.dinheiro = dinheiro
    aposta = 0
    historico = []
    rodadas = []

def apostar(jogador):
    global lucro_cassino
    global saldoacumulado
    if jogador.dinheiro<=20:
        apostado = jogador.dinheiro
    else:
        apostado = 20
    jogador.dinheiro -= apostado
    lucro_cassino += apostado
    saldoacumulado -= apostado
    return apostado
    
## Input dos dados que o usuário quer simular
 
qtd_jogadores = int(input("Quantos jogadores serão simulados?: "))
qtd_dinheiro = int(input("Qual será a quantia de dinheiro inicial de cada jogador?: "))
qtd_rodadas = int(input("Quantas rodadas serão simuladas?: "))
premio = int(input("Qual será o prêmio por vitória? ('35' ou '36'): "))

##Concatenando todos os jogadores em uma lista
jogadores = list()
for i in range(qtd_jogadores):
    jogadores.append(Jogador(qtd_dinheiro))

## Inicializando variáveis
apostas = 0
lucro_cassino = 0
vitorias = 0
qtd_prejuizos = 0
qtd_falencias = 0
saldo = []
rodadas = []
saldoacumulado = qtd_dinheiro*qtd_jogadores

##Simulação das rodadas
saldo.append(saldoacumulado)
rodadas.append(0)
rodada = 1
for i in range(qtd_rodadas):
    sorteado = np.random.randint(0,37)
    for jogador in jogadores:
        if jogador.dinheiro>0:
            apostado = apostar(jogador)
            apostas += 1
            jogador.aposta = np.random.randint(0,37)
            if sorteado == jogador.aposta:
                jogador.dinheiro += apostado*premio + apostado
                lucro_cassino -= apostado*premio + apostado
                saldoacumulado += apostado*premio + apostado
                vitorias += 1
    saldo.append(saldoacumulado)
    rodadas.append(rodada)
    rodada += 1

#Contagem de prejuizos e saldos zerados
for jogador in jogadores:
    if jogador.dinheiro < qtd_dinheiro:
        qtd_prejuizos += 1
    if jogador.dinheiro == 0:
        qtd_falencias += 1
    
##Impressão dos resultados
taxa_vitoria = "{:.3f}".format((vitorias/apostas)*100)
print("\nHOUVERAM ",apostas," APOSTAS, COM APENAS ",vitorias,"VITORIAS.")
print("TAXA DE VITÓRIA: ", taxa_vitoria,"%")
print("DOS {} JOGADORES, {} TERMINARAM O JOGO COM PREJUIZO.".format(qtd_jogadores,qtd_prejuizos))
print("DESTES, {} JOGADORES TERMINARAM O JOGO COM SALDO ZERADO.".format(qtd_falencias))
print("O CASSINO LUCROU R$", lucro_cassino, " NO TOTAL")

#Plotagem do gráfico usando Plotly
dict = {"rodadas": rodadas, "saldo": saldo}
df = pd.DataFrame(dict)
fig = px.line(df, x = "rodadas", y = "saldo", title="Saldo dos jogadores ao longo do tempo", markers = True)
fig.show()