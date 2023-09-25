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
    c1 = (g**y) % p

    # encrypted message
    c2 = ((PK**y) * M) % p

    print("Alice sends: ", c1, c2)

    return c1, c2


def intercept(c1, c2):

    private_key = 0

    for d in range(p):
        if g**d % p == PK:
            private_key = d
            break

    inverse_s = c1**(p-1-private_key)
    m = inverse_s * c2 % p

    print("Intercepted pk: ", private_key, " m:", m)

    return m


def modify(c1, c2):

    modified = (c2*2) % p

    decrypt = c1**(p-1-66) * modified % p

    print("Modified: ", c1, decrypt)

    return c1, modified


def main():
    c1, c2 = encrypt()
    intercept(c1, c2)
    modify(c1, c2)


if __name__ == "__main__":
    main()
