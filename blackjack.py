import numpy as np
import plotly.express as px;
import pandas as pd;

## Classe de jogadores
class Jogador():
    mao = []
    mao_suave = False

##Classe do dealer
class Dealer():
    mao = []
    carta_principal = ''
    dinheiro = 0

##Jogador compra carta
def hit(jogador):
    jogador.mao.append(baralho.pop())

##Embaralhar o deck
def embaralhar():
    np.random.shuffle(baralho)

##Distribui cartas para todos os jogadores e o dealer
def dar_cartas():
    embaralhar()
    for jogador in jogadores:
        jogador.mao.append(baralho.pop())
        jogador.mao.append(baralho.pop())
        jogador.mao_suave = isMao_suave(jogador.mao)
    dealer.mao.append(baralho.pop())
    dealer.carta_principal = dealer.mao[0]
    dealer.mao.append(baralho.pop())

##Calcula o valor de uma mão
def calcular_total(mao):
    total = sum(valores_cartas[carta] for carta in mao)
    for carta in mao:
        if carta == "A" and total>21:
            total -= 10
    return total

##Define se uma mão é suave ou não
def isMao_suave(mao):
    if calcular_total(mao)==17:
        for carta in mao:
            if carta=='A':
                return True
    return False

##Esvazia uma mão
def esvaziar_mao(mao):
    for carta in mao:
        baralho.append(carta)
    nova_mao = []
    return nova_mao
    
##Define o resultado de cada mão dos jogadores em relação ao dealer
def resultado():
    global vitorias, empates, jogadas
    for jogador in jogadores:
        if calcular_total(jogador.mao)<=21 and calcular_total(jogador.mao)>calcular_total(dealer.mao):
            dealer.dinheiro -= 30
            vitorias += 1
        elif calcular_total(jogador.mao)<=21 and calcular_total(jogador.mao)==calcular_total(dealer.mao):
            dealer.dinheiro -= 20
            empates += 1
        elif calcular_total(dealer.mao)>21 and calcular_total(jogador.mao)<=21:
            dealer.dinheiro -= 30
            vitorias += 1
        jogadas += 1
        jogador.mao = esvaziar_mao(jogador.mao)
    dealer.mao = esvaziar_mao(dealer.mao)

##Coleta aposta do jogador
def coletar_aposta():
    dealer.dinheiro += 20

##Faz a jogada de um jogador
def fazer_jogada(jogador):
    if otimizado:
        while jogador.mao_suave and calcular_total(jogador.mao)<18:
            hit(jogador)
        if dealer.carta_principal == '2' or dealer.carta_principal == '3':
            while calcular_total(jogador.mao)<13:
                hit(jogador)
        if dealer.carta_principal == '4' or dealer.carta_principal == '5' or dealer.carta_principal == '6':
            while calcular_total(jogador.mao)<12:
                hit(jogador)
        if dealer.carta_principal == '7' or dealer.carta_principal == '8' or dealer.carta_principal == '9'  or dealer.carta_principal == '10' or dealer.carta_principal == 'A':
            while calcular_total(jogador.mao)<17:
                hit(jogador) 
    else:
        while calcular_total(jogador.mao)<17:
            hit(jogador) 

def printDados():
    print("Número de jogadas: {}".format(jogadas))
    print("Número de vitórias: {}".format(vitorias))
    print("Número de empates: {}".format(empates))
    print("Taxa de vitória: {:.3f}".format((vitorias/jogadas)*100))
    print("Lucro do dealer: {}".format(dealer.dinheiro))

def gerarGrafico(lucro, rodadas):
    otimizado = list()
    for i in range(qtd_rodadas):
        otimizado.append("Não otimizado")
    for i in range(qtd_rodadas):
        otimizado.append("Otimizado")

    dict = {"lucro": lucro, "rodadas": rodadas, "otimizado": otimizado}
    df = pd.DataFrame(dict)
    fig = px.line(df, x = "rodadas", y = "lucro", title="Lucro do dealer ao longo do tempo (jogada otimizada vs não otimizada)", color = otimizado, markers = True)
    fig.show()

#Inicialização do deck - 6 baralhos de 52 cartas
baralho = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4 * 6
valores_cartas = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

##Inicialização de variáveis
jogadores = list()
jogadas = 0
vitorias = 0
empates = 0
lucro = []
rodadas = []
otimizado = False

##Iteração
for jogador in range(7):
    jogadores.append(Jogador())
dealer = Dealer()

qtd_rodadas = int(input("QUANTAS RODADAS A MESA VAI JOGAR?: "))

for rodada in range(qtd_rodadas):
    dar_cartas()
    for jogador in jogadores:
        coletar_aposta()
        fazer_jogada(jogador)
    while calcular_total(dealer.mao)<=17:
        hit(dealer)
    resultado()
    lucro.append(dealer.dinheiro)
    rodadas.append(rodada+1)
print("\nJOGADA NÃO OTIMIZADA: \n")
printDados()
otimizado = True
dealer.dinheiro = 0
vitorias = 0
empates = 0
jogadas = 0
for rodada in range(qtd_rodadas):
    dar_cartas()
    for jogador in jogadores:
        coletar_aposta()
        fazer_jogada(jogador)
    while calcular_total(dealer.mao)<=17:
        hit(dealer)
    resultado()
    lucro.append(dealer.dinheiro)
    rodadas.append(rodada+1)
print("\nJOGADA OTIMIZADA: \n")
printDados()
gerarGrafico(lucro, rodadas)
