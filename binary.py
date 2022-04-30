n = int(input())  # число
d = ''            # строка
while n > 0:
    d = str(n % 2) + d   # при сложении (конкатенации) строк важен порядок.
    # При написаннов в коде варианте число в двоичной системе счисления
    # идёт в нужном порядке, если слагаемые поменять местами
    # так d = d + str(n % 2), то двоичное число окажется записано наоборот, с конца.
    n //= 2
print(d)