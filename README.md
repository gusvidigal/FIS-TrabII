# Relatório do Trabalho II

**Aluno:** Gustavo Vidigal Schulgin  
**RA:** 16814327  
**Disciplina:** Física Básica I - ICMC/USP  
**Professor:** Prof. Dr. Fernando F. Paiva  
**Data:** 14/09/2025

---

## Introdução

O objetivo desse trabalho é resolver um problema inspirado no `Problema conceitual 92` do Capítulo 3 do livro do Tipler:

> **92** Uma bola é lançada de um solo plano a um ângulo de 55° acima da horizontal, com uma rapidez inicial de 22 m/s. Ela cai sobre uma superfície dura e repica, atingindo uma altura máxima igual a 75 por cento daquela atingida no primeiro arco de trajetória. (Ignore a resistência do ar.)
> - **(a)** Qual é a altura máxima atingida no primeiro arco parabólico?
> - **(b)** A que distância horizontal do ponto de lançamento a bola caiu pela primeira vez?
> - **(c)** A que distância horizontal do ponto de lançamento a bola caiu pela segunda vez? Suponha que a componente horizontal da velocidade se mantém constante, na colisão da bola com o chão. \emph{Dica: Você não pode supor que a bola abandonou o chão, após a colisão, a um mesmo ângulo acima da horizontal que no lançamento inicial.}

Adaptei algumas partes do problema para torná-lo mais objetivo e mais difícil:

> Uma bola é lançada de um solo plano a um ângulo `0` acima da horizontal, a uma rapidez inicial `r`. Supondo que, a cada vez que a bola atinge o chão, sua rapidez é reduzida, tornando-se `P` (`0 < P < 1`) da rapidez inicial.
> - **(a)** Qual é o alcance da bola após um quique?  
> - **(b)** E após 50 quiques?  
> - **(c)** Qual é o alcance máximo da bola?  

---

## Raciocínio utilizado

A princípio, temos que nossas variáveis são `0` (o ângulo de lançamento), `r` (a rapidez do lançamento), `P` (o coeficiente de redução da rapidez após cada quique) e `q` (o número de quiques). Podemos, adicionalmente, inserir uma variável `g` para a aceleração da gravidade.

A ideia é utilizar uma linguagem de programação para simular o movimento da bola e calcular os valores pedidos pelo enunciado.

O passo-a-passo é o seguinte:

1. Calcular o movimento da bola no primeiro quique, ou seja, para a rapidez `r` e ângulo `0`.
2. Calcular o movimento da bola no segundo quique, para rapidez `r.p`, ângulo `0` e posição inicial igual à posição final do quique anterior.
3. Repetir os passos anteriores, sempre atualizando a posição inicial dos quiques e reduzindo a rapidez, até obter o número de quiques desejado.

Perceba que o ângulo não é alterado, uma vez estamos considerando que a bolinha é lançada em uma altura `h = 0` e atinge o solo em `h = 0`. Como a trajetória dos quiques pode ser descrita como uma parábola - e parábolas são simétricas - então o ângulo de lançamento será sempre o mesmo. 

---

## Fórmulas físicas utilizadas na resolução

Dada uma rapidez `r` e um ângulo `0`, podemos calcular os módulos dos vetores das velocidades `rx e `ry`:

`rx = r.cos(0)` [1]

`ry = r.sen(0)` [2]

O movimento parabólico da bolinha também pode ser decomposto em duas componentes X e Y:

`Sx = S0x + rx.t` [3]

`Sy = S0y + ry.t - g.t²/2` [4]

Observe, aliás, que `S0y` é sempre `0`.

---

## Resolução do Problema utilizando Python

O código pode ser acessado por meio desse [GitHub - FIS-TrabII](https://github.com/gusvidigal/FIS-TrabII)

### Introdução
Foi utilizada a linguagem de programação Python (versão `3.12.3`) para resolver o exercício.

O algoritmo envolve iterar `q` vezes e calcular a trajetória da bolinha para a rapidez `r.p^(i-1)`, onde `1 <= i <= q` é a i-ésima execução/movimento parabólico que a bolinha executa. As funções `x(t)` e `y(t)` calculam as posições `x` e `y` da bolinha, respectivamente, em intervalos de tempo `dt = 0.0001s`.

Os pontos da trajetória da bolinha são plotados em um gráfico utilizando a biblioteca `matplotlib` para visualização adicional.

### Implementação e comentários do código
#### Bibliotecas
As bibliotecas utilizadas serão a `math` (padrão) - para cálculos trigonométricos - e a `matplotlib` - para plotagem do gráfico

```python
import matplotlib.pyplot as plt
from math import sin, cos, radians, trunc
```

#### Variáveis
Em seguida, o usuário pode inserir as variáveis que desejar para o problema.

```python
#Variáveis globais
g = 10 #aceleração da gravidade
teta = 10 #ângulo de lancamento
r = 10 #rapidez inicial
p = 0.75 #redução da rapidez
quiques = 50 #número de quiques
```

#### Funções físicas
As funções `x` e `y` possuem, como parâmetros, as rapidezes `rx` e `ry`, respectivamente, o instante e as posições iniciais `s0x` e `s0y`. Elas são implementações diretas das equações `[3]` e `[4]`.

Já a função `vel` calcula as componentes `ry` e `ry` da rapidez, dados `r` e `0`. Elas também são implementações diretas das equações `[1]` e `[2]`. É importante ressaltar, aqui, que `0` é dado em graus.

```python
#Funções que definem a posição a partir de Vx e Vy
def x(rx, tempo, s0):
    return rx*tempo + s0
def y(ry, tempo, s0):
    return ry*tempo - (g/2)*tempo**2 + s0
#Componentes rx e ry a partir da rapidez
def vel(rapidez, teta):
    rad = radians(teta)
    return arredondar(cos(rad), 5)*rapidez, arredondar(sin(rad), 5)*rapidez
```

A função `cos()`, da `math`, por causa de aproximações e cálculos feitos pela própria linguagem Python, estava retornando `6.10^(-7)` para `cos(pi)`. Por isso, decidi implementar uma função de arredondamento, que arredonda esse valor para `0`:

```python
#Função de arredondamento
def arredondar(valor, precisao):
    v = valor*(10**precisao)
    if v - trunc(v) >= 0.5:
        return trunc(v+1)/(10**precisao)
    else:
        return trunc(v)/(10**precisao)
```

#### Cálculo dos quiques

O cálculo dos quiques é feito a partir da função mostrada abaixo. A função `calcPos()` calcula todos os quiques requisitados para a função, dados `0`, `q`, `r` e `p`.

Para cada quique, o programa calcula o ponto da trajetória da bolinha no instante seguinte (a partir de 0, os instantes são em intervalos de `0.0001s`) - utilizando as funções `vel` para cálculo das componentes da rapidez e `x` e `y` para a posição. Por fim, o programa adiciona esses pontos da trajetória em dois vetores `pontosX` e `pontosY` - para plotagem posterior.

Caso a bolinha atinja o chão (caso em que sua posição em y é menor ou igual a 0), então a iteração para, a rapidez é reduzida e a posição inicial `s0` (na componente x) é atualizada.

A variável `tempo` representa o instante relativo ao início da trajetória naquele quique, e não o tempo decorrido desde o lançamento inicial.

```python
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
```

#### Execução
A execução do programa se dá de forma simples com o seguinte trecho, o qual é responsável por calcular a trajetória, imprimir o alcance e plotar o gráfico.

```python
pontosX, pontosY, alcance = calcPos(teta, quiques, r, p)
print("Alcance:", alcance)
plt.scatter(pontosX, pontosY, s=1)
```
### Resolução dos itens a), b) e c)

Como o programa permite uma resolução com quaisquer variáveis, iremos utilizar, como exemplo, os valores `r = 10 m/s`, `g = 10 m/s²`, `0 = 45` e `p = 75%`.

1. Para `quiques = 1`, temos um alcance de `3.42 m`.
2. Para `quiques = 50`, temos um alcance de `7.82 m`.
3. Podemos definir um número de quiques arbitrariamente grande. Para `quiques = 100000`, temos um alcance de `7.82 m` (com um pouco mais de aproximação). Isso significa que, com 50 quiques, a bolinha já se movimenta pouco horizontalmente.

![Trajetória da bolinha](https://drive.google.com/uc?export=view&id=1dslxLnTf2a5ZwEG8mo0Wa82wP9wlSk5k)

Trajetória da bolinha, para 100000 quiques

---
