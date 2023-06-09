#!/bin/env python3

dossier ="C:/Users/Zeynep/Downloads/livres_2"
chemin_rapports="C:/Users/Zeynep/Downloads/Rapports"


from bibliotheque import Trier

filesPDF=Trier(dossier).DocumentsPDF # ---> on obtient la liste des chemins d'accès de tous les fichiers pdf
filesEpub=Trier(dossier).DocumentsEpub # ---> on obtient la liste des chemins d'accès de tous les fichiers epub




from bibliotheque import PDF

livrepdf = PDF("C:/Users/Zeynep/Downloads/livres/hugo_notre_dame_de_paris.pdf")
print(livrepdf.titre)
print(livrepdf.toc())




from bibliotheque import Epub

livreepub = Epub("C:/Users/Zeynep/Downloads/livres/hugo_victor_-_han_d_islande.epub")
print(livreepub.auteur)
print(livreepub.toc())




from bibliotheque import Livres

l=Livres(filesPDF)
print(l)



from bibliotheque import Rapport

r=Rapport(dossier)
r.write(chemin_rapports)
r.ToC(chemin_rapports)

r=Rapport(dossier)
r.MaJ(chemin_rapports)


