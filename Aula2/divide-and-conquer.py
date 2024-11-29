# Arvore binária, é recursiva e vai até ao caso mais simples 2¹
# binária porque vamos dividindo o problema, por exemplo 2⁵ = 2² * 2³ ....


def exponencial(a, b):
    if b == 0:
        return 1
    if b == 1:
        return a
    c = b // 2
    d = b - c
    return exponencial(a, c) * exponencial(a, d)

print(exponencial(2, 3))