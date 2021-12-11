

import math

#ponto para o infinito 
INF_POINT = None

class EllipticCurve:
    def __init__(self,a,b,p,G) -> None:
        # componentes a e b da curva elíptica
        self.a = a
        self.b = b
        # primo
        self.p = p
        # pontos da curva
        self.points = []
        # ponto Gerador para curvas com primos grandes
        self.G = G

    # aqui temos um problemão!!! Não podemos guardar primos muito grandes pois teríamos muitos pontos!
    # para resolver esse problema vamos guardar apenas o ponto gerador! Isso seja, o ponto G que
    # k*G = qualquer outro ponto na curva! Sendo 0 <= k <= n  
    def define_points(self):
        self.points.append(INF_POINT)
        for x in range(self.p):
            for y in range(self.p):
                if self.equal_modp(y*y,x*x*x + self.a*x + self.b):
                    self.points.append((x,y))

    # Para resolver o problema descrito acima vamos fazer uma função que multiplica um ponto k vezes!
    def multiplication(self, k, p):
        x = p
        q = INF_POINT
        if k == 0:
            return q
        # vamos bit a bit em k vendo se o LSB é 0 ou 1. Se for 1 fazemos Q = Q + X
        while k != 0:
            if k & 1 != 0:
                q = self.addition(q,x)
            x = self.addition(x,x)
            k >>= 1
        return q

    #funções auxiliares para a curva

    def print_points(self):
        print(self.points)

    def number_points(self):
        return len(self.points)

    def reduce_modp(self, x):
        return x % self.p
    
    def equal_modp(self, x, y):
        return self.reduce_modp(x - y) == 0

    def is_on_curve(self, x, y):
        return self.equal_modp(y * y, pow(x,3) + self.a * x + self.b)
    
    # aqui fazemos uma busca 'brute-force' pelos pontos que,
    # para primos gigantes, é computacionalmente impossível!!
    def inverse_modp(self, x):
        for y in range(self.p):
            if self.equal_modp(x*y,1):
                return y
        return None

    # aqui melhoramos drasticamente o código!
    # com o pequeno teorema de Fermat temos: se p é primo e x é um natural tal que (x,p) == 1...
    # ... temos que  o inverso do mod x -> x^-1 == x^(p-2)(mod p)
    def inverse_modp_fermat(self, x):
        if x % self.p == 0:
            return None
        return pow(x,self.p-2,self.p)

    def discriminant(self):
        # Discr = (4 * a^3) + (27 * b^2)
        D = 4 * pow(self.a,3) + 27 * pow(self.b,2)
        return self.reduce_modp(D);

    # código para a operação binária com os pontos p1 p2
    # página 3 do paper citado nas ref.
    def addition(self, p1, p2):
        # ponto para o infinito é o elemento identidade!
        if p1 == INF_POINT:
            return p2
        if p2 == INF_POINT:
            return p1

        
        # coordenadas de p1 e p2
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]

        if self.equal_modp(x1,x2) and self.equal_modp(y1,-y2):
            return INF_POINT
        if self.equal_modp(x1,x2) and self.equal_modp(y1,y2):
            # lambda = coeficiente angular da reta que passa em p1 e p2
            #       ... se p1 == p2 então seria a derivada da tangente!
            u = self.reduce_modp((3 * pow(x1,2) + self.a) * self.inverse_modp_fermat(2*y1))
        else:
            # entre 0 e (p - 1)
            u = self.reduce_modp((y1 - y2) * self.inverse_modp_fermat(x1 - x2))
        v = self.reduce_modp(y1 - u * x1)


        # output da opreação
        x3 = self.reduce_modp(pow(u,2) - x1 - x2)
        y3 = self.reduce_modp(-u * x3 - v)

        return (x3,y3)


    #   Testando a propriedade associativa para todas as triplas de pontos na curva!
    #   Se a discriminante é diferente de 0 é garantida essa propriedade
    #   porém é intrutivo testar...
    def test_associativity(self):
        n = self.number_points()
        for i in range (n):
            for j in range (n):
                for k in range (n):
                    P = self.addition(self.points[i],self.addition(self.points[j],self.points[k]))
                    Q = self.addition(self.addition(self.points[i],self.points[j]),self.points[k])
                    if P != Q:
                        return False

        return True

#   Função que conta todas as possívei curvas dado um número de pontos!
def count_all_possible_curves(p):
    count = 0
    for a in range (p):
        for b in range(p):
            ec = EllipticCurve(a,b,p)
            if ec.discriminant() == 0:# se a discriminante for 0 não somamos como uma curva válida
                continue
            count += 1
    return count



def main():
    # Vamos comuptar, seguindo o modelo da página 11 seção 6.4.2 do artigo, uma curva que Micheal e Nikita concordam!
    p = 785963102379428822376694789446897396207498568951
    a = 317689081251325503476317476413827693272746955927
    b = 79052896607878758718120572025718535432100651934
    G = (771507216262649826170648268565579889907769254176, 390157510246556628525279459266514995562533196655)

    # Criando a curva elíptica para os dados acima
    ec = EllipticCurve(a,b,p,G) 
    
    # Chave privada de Nikita!
    n = 670805031139910513517527207693060456300217054473

    # Vamos checar se o G esta correto? Para isso vemos se ele pelo menos está presente na curva...
    print()
    print('G está na cruva? ',end="")
    print(ec.is_on_curve(G[0],G[1]))
    # Seguindo... pela teoria sabemos que o Gerador * 0 tem que resultar em INF_POINT (None) certo? então vamos testar!
    print('G * 0 = ',end="")
    print(ec.multiplication(0,G))
    print()
    # No arquivo encriptado temos um par de pontos: (rB, P + r(nB)) onde B é o ponto gerador
    rB = (179671003218315746385026655733086044982194424660, 697834385359686368249301282675141830935176314718)
    PplusrnB =  (137851038548264467372645158093004000343639118915, 110848589228676224057229230223580815024224875699)

    # Computamos n*(rB) com nossa chave secreta 
    nrB = ec.multiplication(n,rB)
    # se compararmos com o artigo vemos que computamos nrB corretamente!!
    print(f"calculando n*(rB) = {nrB}")
    print()
    # Agora para obter a chave para desbloquear o conteúdo encriptado vamos fazer P + r(nB) - n(rB)
    P = (14489646124220757767, 669337780373284096274895136618194604469696830074) # P do artigo
    # Vamos ver se P calculado é igual...
    Pcalculado = ec.addition(PplusrnB,(nrB[0],ec.reduce_modp(-nrB[1])))
    if Pcalculado == P:
        print('Deu certo! Deciframos corretamente o P')

    # Com isso temos a chave de acesso! Podemos decriptar o arquivo a vontade!
    print(f"Chave de acesso computada:{Pcalculado[0]}")


    # Para fechar com chave de ouro! Vamos ver se P + n(rB) calculado vai ser igual ao P + r(nB) dado no início!!
    print('P(calculado) + r(nB)(também calculado) é igual ao P + r(nB) dado? ',end="")
    print(ec.addition(nrB,Pcalculado) == PplusrnB)
    




if __name__ == '__main__':
    main()

