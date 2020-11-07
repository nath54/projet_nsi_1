
import os
import io

auteurs = {}

def examine(fich):
    print(fich)
    #
    f = io.open(fich, 'r', encoding = "utf-8")
    txt = f.read().lower()
    f.close()
    #
    ta = "auteur: "
    pos = txt.find(ta)
    while pos != -1 and pos < len(txt):
        #
        fin_aut = txt.find("\n", pos)
        deb_f = txt.rfind("def", pos)
        if deb_f != -1 and fin_aut != -1:
            fin_f = txt.find("(", deb_f)
            #
            aut = txt[pos:fin_aut]
            fn = fich+ " - " + txt[deb_f+3: fin_f]
            #
            if aut in auteurs.keys():
                auteurs[aut].append(fn)
            else:
                auteurs[aut] = [fn]
        #
        pos = txt.find(ta, pos + 1)


def parc(path):
    for fi in os.listdir(path):
        if fi.endswith(".py"):
            examine(path + fi)
        elif os.path.isdir(path + fi):
            parc(path + fi + "/")

def ecrit():
    txt = ""
    for a in auteurs.keys():
        txt += "\n\n" + a + ":"
        for fn in auteurs[a]:
            txt+= "\n  - " + fn
    #
    print(txt)
    #
    f = io.open("quiafaitquoi.md", 'w', encoding = "utf-8")
    f.write(txt)
    f.close()

def main():
    parc("./")
    #
    ecrit()
   
if __name__ == "__main__":
    main()
