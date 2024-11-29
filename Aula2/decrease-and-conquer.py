def exponencial(a, b):
    if b == 0:
        return 1
    return a * exponencial(a, b-1)

print(exponencial(2, 3))


# extra task

# 2⁵ = 2 * 2² * 2²
# ou seja pergunto se é par ou impar

# quantas multiplicações preciso de fazer neste tipo de algoritmo (par e impar)?
# coloca-se o valor de b em binário, elimina-se o bit da esquerda e soma se os restantes, sendo que 0 = 1 e 1 = 2
# ou seja para b = 11 -> binário 1011, 1 + 2 + 2, 5 multiplicações


def exponencial2(a, b):
    if b == 0:
        return 1
    if b == 1:
        return a
    if b % 2 == 0:
        return exponencial2(a, b/2) * exponencial2(a, b/2)
    return a * exponencial2(a, b-1)

print(exponencial2(2, 3))
  