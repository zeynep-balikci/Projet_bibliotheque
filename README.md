Nous avions à notre disposition un dossier de 20 Go qui contenait plusieurs fichiers de différents types ainsi que quelques dossiers de fichiers MP4. 

En lisant le chemin de ce dossier à partir d'un fichier "bibli.conf", et où il y avait également le chemin du dossier où déposer les rapports que nous devions créer, la commande suivante dans le shell devrait générer ces rapports sur les livres de notre "bibliothèque" :

```
./bibli.py init
```

Ou bien un autre fichier .conf (où 1er ligne : le chemin du dossier contenant tout les fichiers à traiter, 2e ligne : le chemin dossier où déposer les fichiers que nous devions créer):

```
./bibli.py init -c bibli.conf
```

La commande suivante met à jour les rapports que nous avons créer :

```
./bibli.py update
```

Les rapports générés sont :
- la liste des auteurs (i.e. le nom de chaque auteur, le titre de ses livres et le nom du fichier de ces livres) sous format txt, pdf et epub.
- la liste des ouvrages (i.e. le titre de chaque livre, l'auteur, la langue et le nom du fichier) sous format txt, pdf et epub.
- la table des matières de chaque livre sous format txt, pdf et epub.
