import math
pi = 3.141592653589793238462643383279502884197169399375105820974944592307816406286

def GregoryLeibniz():
    # Time: O(N * logN * loglogN)
    calc = 0
    iter = 1000
    for i in range(iter):
        demoninator = 2 * i + 1
        if (i % 2 != 1):
            calc = calc + 4 / demoninator
        else:
            calc = calc - 4 / demoninator
    print(f'GregL Pi-{iter}: {calc} {(pi - calc) / pi * 100:.6f}%')

def nilakantha():
    # Formula:
    # Time: O(N * logN * loglogN)
    calc = 3
    iter = 100
    for i in range(iter):
        base = 2 * (i + 1)
        demoninator = (base + 0) * (base + 1) * (base + 2)
        if (i % 2 != 1):
            calc = calc + 4 / demoninator
        else:
            calc = calc - 4 / demoninator
    print(f'nilak Pi-{iter}: {calc} {(pi - calc) / pi * 100:.6f}%')

def ramanujan_pi():
    # O(N2 logN loglogN)
    sum = 0
    n   = 0
    i   = (math.sqrt(8)) / 9801     # 2√2/(99)^2

    while True:
        # Ramanujan's Formula:-
        tmp = i * (factorial(4 * n) / pow(factorial(n), 4)) * ((26390 * n + 1103) / pow(396, 4 * n))
        sum += tmp

        if(abs(tmp) < 1e-15):        # Stop loop when it reaches 15th digit precision (femto)
            break
        n += 1
    print(f'raman Pi-{n}: {1 / sum} {(pi - 1 / sum) / pi * 100:.6f}%')

    return(1 / sum)

def factorial(x):
    if x == 0:
        return 1
    else:
        return x * factorial(x - 1)


GregoryLeibniz()
nilakantha()
ramanujan_pi()
