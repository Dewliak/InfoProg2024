
def megoldas(n ,s):

    i f(s == 0):
        return 1

    suma = 0

    for i in range(1 ,min(n ,s)):
        suma += megoldas(n, s- i)

    return suma


if __name__ == "__main__":
    print(megoldas(6, 4))



