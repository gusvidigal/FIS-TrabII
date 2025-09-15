import matplotlib.pyplot as plt
from math import sin, cos, radians, trunc

#Variáveis globais
g = 10 #aceleração da gravidade
teta = 10 #ângulo de lancamento
r = 10 #rapidez inicial
p = 0.75 #redução da rapidez
quiques = 100000 #número de quiques

#Função de arredondamento
def arredondar(valor, precisao):
    v = valor*(10**precisao)
    if v - trunc(v) >= 0.5:
        return trunc(v+1)/(10**precisao)
    else:
        return trunc(v)/(10**precisao)

#Funções que definem a posição a partir de Vx e Vy
def x(rx, tempo, s0):
    return rx*tempo + s0
def y(ry, tempo, s0):
    return ry*tempo - (g/2)*tempo**2 + s0
#Componentes rx e ry a partir da rapidez
def vel(rapidez, teta):
    rad = radians(teta)
    return arredondar(cos(rad), 5)*rapidez, arredondar(sin(rad), 5)*rapidez

#Calcula os quiques
def calcPos(teta, quiques, r, p):
    pontosX = []
    pontosY = []
    rapidez = r
    tempo = 0
    s0 = 0
    #Para cada quique
    for q in range(0, quiques):
        #Calcula os pontos até encostar o chão de novo
        while True:
            rx, ry = vel(rapidez, teta)
            sx = x(rx, tempo, s0)
            sy = y(ry, tempo, 0)
            #Verifica se encostou o chão e define nova posição inicial
            if sy < 0:
                s0 = sx
                break
            #Adiciona na plotagem
            pontosX.append(sx)
            pontosY.append(sy)
            #Incrementa tempo
            tempo += 0.0001
        #Redução da rapidez e redefinição do tempo (para iniciar uma nova parábola)
        rapidez *= p
        tempo = 0
    #retorna 2 vetores das componentes X e Y dos pontos e o alcance
    return pontosX, pontosY, max(pontosX)

pontosX, pontosY, alcance = calcPos(teta, quiques, r, p)
print("Alcance:", alcance)
plt.scatter(pontosX, pontosY, s=1)

'''
#PARTE OPCIONAL: Plotar vários gráficos ao mesmo tempo
for teta in [15, 30, 45, 60, 75]:
    pontosX, pontosY, alcance = calcPos(teta, quiques)
    plt.scatter(pontosX, pontosY, s=1)
'''
plt.show()

