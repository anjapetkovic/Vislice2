def je_prastevilo(n):
    """Fukcija, ki pove, ali je podano število praštevilo."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    kandidat_za_delitelja = 3
    while kandidat_za_delitelja ** 2 <= n:
        if n % kandidat_za_delitelja == 0:
            return False
        else:
            kandidat_za_delitelja += 2
    return True

for i in range(200):
    if je_prastevilo(i):
        print(i)
        print(i)