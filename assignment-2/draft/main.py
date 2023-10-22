import random


def dealer():
    max = 2048
    s = random.randint(1, max)

    s1 = random.randint(1, max)
    s2 = random.randint(1, max)
    s3 = s + max - ((s1 + s2) % max)

    print("s: ", s, " s1: ", s1, " s2: ", s2, " s3: ", s3)

    return s1, s2, s3


dealer()
