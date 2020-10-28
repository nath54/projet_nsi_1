import random

t=""
while t!="q":
    t=input("> ")
    if t!="q":
        t=list(t)
        random.shuffle(t)
        print("".join(t))

