
#ponto para o infinito 
INF_POINT = None

class EllipticCurve:
    def __init__(self,a,b,p) -> None:
        self.a = a
        self.b = b
        self.p = p
        self.points = []
        self.define_points()

    def define_points(self):
        self.points.append(INF_POINT)
        for x in range(self.p):
            for y in range(self.p):
                if self.equal_modp(y*y,x*x*x + self.a*x + self.b):
                    self.points.append((x,y))

    #funções auxiliares para a curva

    def print_points(self):
        print(self.points)

    def number_points(self):
        return len(self.points)

    def reduce_modp(self, x):
        return x % self.p
    
    def equal_modp(self, x, y):
        return self.reduce_modp(x - y) == 0
    
    def inverse_modp(self, x):
        for y in range(self.p):
            if self.equal_modp(x*y,1):
                return y
        return None

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
            u = self.reduce_modp((3 * pow(x1,2) + self.a) * self.inverse_modp(2*y1))
        else:
            # entre 0 e (p - 1)
            u = self.reduce_modp((y1 - y2) * self.inverse_modp(x1 - x2))
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
    ec = EllipticCurve(2,7,19)
    p3 = ec.addition(ec.points[5],ec.points[14])
    p = 19
    print(f"Número de curvas possiveis com p {p}: {count_all_possible_curves(p)}")

if __name__ == '__main__':
    main()