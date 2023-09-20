import random

# public shared base
g = 666

# public shared prime
p = 6661

# Bob public key
PK = 2227

# Alice message
M = 2000


def encrypt():
    # Alice´s y
    y = random.randint(1, p-1)

    # g^y mod p
    fst_par = (g**y) % p

    # encrypted message
    c = ((PK**y) * M) % p

    print("Alice sends: ", fst_par, c)

    return fst_par, c


def intercept(fst_par, c):

    private_key = 0

    for d in range(p):
        if g**d % p == PK:
            private_key = d
            break

    print("Guessed private key: ", private_key)

    m = c / ((fst_par**private_key) % p)

    print("Intercepted message: ", m)

    return m


def main():
    fst_par, c = encrypt()
    intercept(fst_par, c)


if __name__ == "__main__":
    main()
