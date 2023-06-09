#!/bin/env python3
import sys
from bibliotheque import Rapport
"""
Nous avons décidé d'utiliser notre propre module
"""
if __name__ == "__main__":
    conf="bibli.conf"
    if sys.argv[1]=="-c":
        conf=sys.argv[2]
    f = open(conf, "r")

    lines=f.readlines()
    dossier=lines[0].replace("\n","")
    chemin_rapports=lines[1]
    r=Rapport(dossier)

    if "init" in sys.argv:
        r.write(chemin_rapports)
        r.ToC(chemin_rapports)

    elif "update" in sys.argv:
        r.MaJ(chemin_rapports)
