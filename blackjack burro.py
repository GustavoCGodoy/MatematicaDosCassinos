import numpy as np
import plotly.express as px;
import pandas as pd;

class Jogador():
    mao = []
    total = 0
    mao_suave = False
        
class Dealer():
    mao = []
    carta_principal = ''
    dinheiro = 0

baralho = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4 * 6
valores_cartas = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

qtd_rodadas = int(input("QUANTAS RODADAS A MESA VAI JOGAR?: "))
jogadores = list()
jogadas = 0
vitorias = 0
empates = 0
lucro = []
rodadas = []

def hit(jogador):
    jogador.mao.append(baralho.pop())

def embaralhar():
    np.random.shuffle(baralho)

def dar_cartas():
    embaralhar()
    for jogador in jogadores:
        jogador.mao.append(baralho.pop())
        jogador.mao.append(baralho.pop())
        jogador.mao_suave = isMao_suave(jogador.mao)
    dealer.mao.append(baralho.pop())
    dealer.carta_principal = dealer.mao[0]
    dealer.mao.append(baralho.pop())

def calcular_total(mao):
    total = sum(valores_cartas[carta] for carta in mao)
    for carta in mao:
        if carta == "A" and total>21:
            total -= 10
    return total

def isMao_suave(mao):
    if calcular_total(mao)==17:
        for carta in mao:
            if carta=='A':
                return True
    return False

def esvaziar_mao(mao):
    for carta in mao:
        baralho.append(carta)
    nova_mao = []
    return nova_mao
    
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
    
def coletar_aposta():
    dealer.dinheiro += 20

def fazer_jogada(jogador):
    while calcular_total(jogador.mao)<17:
        hit(jogador) 

for jogador in range(7):
    jogadores.append(Jogador())
dealer = Dealer()

for rodada in range(qtd_rodadas):
    dar_cartas()
    for jogador in jogadores:
        coletar_aposta()
        fazer_jogada(jogador)
    while calcular_total(dealer.mao)<=17:
        hit(dealer)
    resultado()
    lucro.append(dealer.dinheiro)
    rodadas.append(rodada)

print("Número de jogadas: {}".format(jogadas))
print("Número de vitórias: {}".format(vitorias))
print("Número de empates: {}".format(empates))
print("Taxa de vitória: {:.3f}".format((vitorias/jogadas)*100))

dict = {"lucro": lucro, "rodadas": rodadas}
df = pd.DataFrame(dict)
fig = px.line(df, x = "rodadas", y = "lucro", title="Lucro do dealer ao longo do tempo (jogadores param ao fazer 17)", markers = True)
fig.show()