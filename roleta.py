import numpy;
import plotly.express as px;
import pandas as pd;

class Jogador:
    def __init__(self, dinheiro, aposta):
        self.dinheiro = dinheiro;
        self.aposta = aposta;
    historico = [];
    rodadas = [];
## njogadores = input("Insira o número de jogadores: ");

objs = list();
for i in range(10):
    objs.append(Jogador(1000,0));
apostas = 0;
vitorias = 0;
historicogeral = [];
group = [];
rodadasgeral = [];
for i in range(50):
    sorteado = numpy.random.randint(0,37)
    print("Na rodada ",i+1," o número sorteado foi: ",sorteado)
    j = 0;
    for jogador in objs:
        historicogeral.append(jogador.dinheiro);
        rodadasgeral.append(i);
        group.append(j);
        if jogador.dinheiro>0:
            jogador.dinheiro -= 20
            apostas += 1
            jogador.aposta = numpy.random.randint(0,37)
            if sorteado == jogador.aposta:
                jogador.dinheiro += 700
                vitorias += 1
        j+=1;
print("HOUVERAM ",apostas," APOSTAS, COM APENAS ",vitorias,"VITORIAS");
for jogador in objs:
    print("O DINHEIRO DO JOGADOR É ", jogador.dinheiro);

fig = px.line(x = rodadasgeral, y = historicogeral, color = group);
fig.show()