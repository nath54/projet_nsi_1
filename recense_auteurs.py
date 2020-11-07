
import os
import io

auteurs = {}


def examine(fich):
    print(fich)
    #
    f = io.open(fich, 'r', encoding="utf-8")
    txt = f.read()  # .lower()
    f.close()
    #
    ta = "Auteur: "
    pos = txt.find(ta, 0)
    while pos != -1:
        #
        fin_aut = txt.find("\n", pos)
        #
        deb_f = -1
        pa = pos
        while pa > 3:
            if txt[pa - 3: pa] == "def":
                deb_f = pa
            pa -= 1
        #
        # deb_f = txt.rfind("def", pos)
        if deb_f != -1:
            print(pos)
            fin_f = txt.find("(", deb_f)
            #
            aut = txt[pos + len(ta):fin_aut]
            fn = fich + " - " + txt[deb_f: fin_f]
            #
            if aut in auteurs.keys():
                #if fn not in auteurs[aut]:
                    auteurs[aut].append(fn)
            else:
                auteurs[aut] = [fn]
        #
        pos = txt.find(ta, pos + 1)


def parc(path):
    fichs = os.listdir(path)
    print([f for f in fichs if f.endswith(".py")])
    for fi in fichs:
        if fi.endswith(".py"):
            examine(path + fi)
        elif os.path.isdir(path + fi):
            parc(path + fi + "/")


def ecrit():
    txt = ""
    for a in auteurs.keys():
        txt += "\n\n" + a + ":"
        for fn in auteurs[a]:
            txt += "\n  - " + fn
    #
    print(txt)
    #
    f = io.open("quiafaitquoi.md", 'w', encoding="utf-8")
    f.write(txt)
    f.close()


def main():
    parc("./")
    #
    ecrit()


if __name__ == "__main__":
    main()
