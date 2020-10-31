import random

t = ""
while t != "q":
    t = input("> ")
    if len(t) > 1:
        tt = list(t)
        reps = list()
        for _ in range(10):
            random.shuffle(tt)
            reps.append(("".join(tt)).lower())
        reps = list(set(sorted(reps)))
        aff = "  - " + "\n  - ".join([r[0].upper() + r[1:] for r in reps])
        print(f"Voici une liste d'anagrames de {t} :\n{aff}")
