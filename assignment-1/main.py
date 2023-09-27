import random


def prt(g, p, PK, p1, p2, p3):
    print(p1, "\t[", g, ",", p, ",", PK, ",", p2, ",", p3, "]")


def encrypt(g, p, PK, M):
    # Alice´s y
    y = random.randint(1, p-1)

    # g^y mod p
    c1 = (g**y) % p

    # encrypted message
    c2 = ((PK**y) * M) % p

    return "Alice sends:", c1, c2


def intercept(g, p, PK, c1, c2):

    private_key = 0

    for d in range(p):
        if g**d % p == PK:
            private_key = d
            break

    inverse_s = c1**(p-1-private_key)
    m = inverse_s * c2 % p

    return "Intercepted:", private_key, m


def modify(p, c1, c2):

    modified = (c2*2) % p

    return "Modified", c1, modified


def main():
    g = 666  # public shared base
    p = 6661  # public shared prime
    PK = 2227  # Bob public key
    M = 2000  # Alice message

    print("\n")
    str, c1, c2 = encrypt(g, p, PK, M)
    prt(g, p, PK, str, c1, c2)
    print("\n")

    str, a, b = intercept(g, p, PK, c1, c2)
    prt(g, p, PK, str, a, b)
    print("\n")

    str, a, c2m = modify(p, c1, c2)
    prt(g, p, PK, str, a, b)
    _, a, b = intercept(g, p, PK, c1, c2m)
    prt(g, p, PK, "Decrypted´", a, b)


if __name__ == "__main__":
    main()
