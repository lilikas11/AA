def exponencial(a, b):
    result = 1
    for i in range(b):
        result = result * a
    return result

print(exponencial(2, 3))