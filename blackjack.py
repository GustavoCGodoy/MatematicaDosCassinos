import numpy as np
import plotly.express as px;
import pandas as pd;

## Classe de jogadores
class Jogador():
    mao = []
    mao_split = []
    mao_suave = False
    blackjack = False
    blackjack_split = False

##Classe do dealer
class Dealer():
    mao = []
    carta_principal = ''
    dinheiro = 0

##Jogador compra carta
def hit(jogador):
    jogador.mao.append(baralho.pop())

def hit_split(jogador):
    jogador.mao_split.append(baralho.pop())

##Embaralhar o deck
def embaralhar():
    np.random.shuffle(baralho)

##Distribui cartas para todos os jogadores e o dealer
def dar_cartas():
    global cartas_usadas
    if cartas_usadas>=208:
        embaralhar()
        cartas_usadas = 0
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

#Checa se uma mão é um par
def isPar(mao):
    if mao[0] == mao[1]:
        return mao[0]
    else:
        return False
    
def isBlackjack(jogador):
    if len(jogador.mao)==2 and calcular_total(jogador.mao)==21:
        jogador.blackjack = True
    else:
        jogador.blackjack = False

def isBlackjack_split(jogador):
    if len(jogador.mao_split)==2 and calcular_total(jogador.mao_split)==21:
        jogador.blackjack_split = True
    else:
        jogador.blackjack_split = False

##Checa se o jogador precisa fazer split
def split(jogador):
    if (isPar(jogador.mao) == '2' or isPar(jogador.mao) == '3') and (dealer.carta_principal == '4' or dealer.carta_principal == '5' or dealer.carta_principal == '6' or dealer.carta_principal == '7'):
        jogador.mao_split.append(jogador.mao.pop())
        dealer.dinheiro += 20
        fazer_jogada_split(jogador)
    elif isPar(jogador.mao) == '6' and (dealer.carta_principal == '3' or dealer.carta_principal == '4' or dealer.carta_principal == '5' or dealer.carta_principal == '6'):
        jogador.mao_split.append(jogador.mao.pop())
        dealer.dinheiro += 20
        fazer_jogada_split(jogador)
    elif (isPar(jogador.mao)=='7' or isPar(jogador.mao)=='8') and (dealer.carta_principal=='2' or  dealer.carta_principal=='3' or dealer.carta_principal=='4' or dealer.carta_principal=='5' or dealer.carta_principal=='6' or dealer.carta_principal=='7'):
        jogador.mao_split.append(jogador.mao.pop())
        dealer.dinheiro += 20
        fazer_jogada_split(jogador)
    elif (isPar(jogador.mao)=='8' or isPar(jogador.mao)=='9') and (dealer.carta_principal=='8' or  dealer.carta_principal=='9'):
        jogador.mao_split.append(jogador.mao.pop())
        dealer.dinheiro += 20
        fazer_jogada_split(jogador)
    elif (isPar(jogador.mao)=='9') and (dealer.carta_principal=='2' or  dealer.carta_principal=='3' or dealer.carta_principal=='4' or dealer.carta_principal=='5' or dealer.carta_principal=='6'):
        jogador.mao_split.append(jogador.mao.pop())
        dealer.dinheiro += 20
        fazer_jogada_split(jogador)
    elif (isPar(jogador.mao)=='A') and (dealer.carta_principal=='2' or  dealer.carta_principal=='3' or dealer.carta_principal=='4' or dealer.carta_principal=='5' or dealer.carta_principal=='6' or dealer.carta_principal=='7' or dealer.carta_principal=='8' or dealer.carta_principal=='9' or dealer.carta_principal=='10'):
        jogador.mao_split.append(jogador.mao.pop())
        dealer.dinheiro += 20
        fazer_jogada_split(jogador)

##Esvazia uma mão
def esvaziar_mao(mao):
    global cartas_usadas
    for carta in mao:
        baralho.insert(0, carta)
        cartas_usadas += 1
    nova_mao = []
    return nova_mao
    
##Define o resultado de cada mão dos jogadores em relação ao dealer
def resultado():
    global vitorias, empates, jogadas, blackjack
    for jogador in jogadores:
        if jogador.blackjack and calcular_total(dealer.mao)!=21:
            dealer.dinheiro -= 50
            vitorias += 1
            blackjack += 1
        elif calcular_total(jogador.mao)<=21 and calcular_total(jogador.mao)>calcular_total(dealer.mao):
            dealer.dinheiro -= 40
            vitorias += 1
        elif calcular_total(jogador.mao)<=21 and calcular_total(jogador.mao)==calcular_total(dealer.mao):
            dealer.dinheiro -= 20
            empates += 1
        elif calcular_total(dealer.mao)>21 and calcular_total(jogador.mao)<=21:
            dealer.dinheiro -= 40
            vitorias += 1
        jogadas += 1
        jogador.mao = esvaziar_mao(jogador.mao)
    dealer.mao = esvaziar_mao(dealer.mao)

##Define o resultado de cada mão dos jogadores em relação ao dealer
def resultado_split():
    global vitorias, empates, jogadas, blackjack
    for jogador in jogadores:
        if jogador.mao_split:
            if jogador.blackjack_split and calcular_total(dealer.mao)!=21:
                dealer.dinheiro -= 50
                vitorias += 1
                blackjack += 1
            elif calcular_total(jogador.mao_split)<=21 and calcular_total(jogador.mao_split)>calcular_total(dealer.mao):
                dealer.dinheiro -= 40
                vitorias += 1
            elif calcular_total(jogador.mao_split)<=21 and calcular_total(jogador.mao_split)==calcular_total(dealer.mao):
                dealer.dinheiro -= 20
                empates += 1
            elif calcular_total(dealer.mao)>21 and calcular_total(jogador.mao_split)<=21:
                dealer.dinheiro -= 40
                vitorias += 1
            jogadas += 1
            jogador.mao_split = esvaziar_mao(jogador.mao_split)

##Coleta aposta do jogador
def coletar_aposta():
    dealer.dinheiro += 20

##Faz a jogada de um jogador
def fazer_jogada(jogador):
    isBlackjack(jogador)
    if otimizado and isMao_suave(jogador.mao):
        split(jogador)
        while calcular_total(jogador.mao)<=17:
            hit(jogador)
        while (dealer.carta_principal == '9' or dealer.carta_principal == '10' or dealer.carta_principal == 'A') and calcular_total(jogador.mao) == 18:
            hit(jogador)
    elif otimizado:
        split(jogador)
        while calcular_total(jogador.mao)<=11:
            hit(jogador)
        while (dealer.carta_principal == '2' or dealer.carta_principal == '3') and calcular_total(jogador.mao)==12:
            hit(jogador)
        while (dealer.carta_principal == 'A' or dealer.carta_principal == '7' or dealer.carta_principal == '8' or dealer.carta_principal == '9' or dealer.carta_principal == '10') and calcular_total(jogador.mao)<=16:
            hit(jogador)
    else:
        while calcular_total(jogador.mao)<17:
            hit(jogador) 

def fazer_jogada_split(jogador):
    hit_split(jogador)
    isBlackjack_split(jogador)
    if isMao_suave(jogador.mao_split):
        while calcular_total(jogador.mao_split)<=17:
            hit_split(jogador)
        while (dealer.carta_principal == '9' or dealer.carta_principal == '10' or dealer.carta_principal == 'A') and calcular_total(jogador.mao_split) == 18:
            hit_split(jogador)
    else:
        while calcular_total(jogador.mao_split)<=11:
            hit_split(jogador)
        while (dealer.carta_principal == '2' or dealer.carta_principal == '3') and calcular_total(jogador.mao_split)==12:
            hit_split(jogador)
        while (dealer.carta_principal == 'A' or dealer.carta_principal == '7' or dealer.carta_principal == '8' or dealer.carta_principal == '9' or dealer.carta_principal == '10') and calcular_total(jogador.mao_split)<=16:
            hit_split(jogador)

def printDados():
    print("Número de jogadas: {}".format(jogadas))
    print("Número de blackjacks: {}".format(blackjack))
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
blackjack = 0
cartas_usadas = 0
jogadas = 0
vitorias = 0
empates = 0
derrotas = 0
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
    while calcular_total(dealer.mao)<17:
        hit(dealer)
    resultado()
    lucro.append(dealer.dinheiro)
    rodadas.append(rodada+1)
print("\nJOGADA NÃO OTIMIZADA: \n")
printDados()
otimizado = True
dealer.dinheiro = 0
blackjack = 0
vitorias = 0
empates = 0
jogadas = 0
derrotas = 0
for rodada in range(qtd_rodadas):
    dar_cartas()
    for jogador in jogadores:
        coletar_aposta()
        fazer_jogada(jogador)
    while calcular_total(dealer.mao)<17:
        hit(dealer)
    resultado_split()
    resultado()
    lucro.append(dealer.dinheiro)
    rodadas.append(rodada+1)
print("\nJOGADA OTIMIZADA: \n")
printDados()
gerarGrafico(lucro, rodadas)
