Nous avions à notre disposition un dossier de 20 Go qui contenait plusieurs fichiers de différents types ainsi que quelques dossiers de fichiers MP4. 

En lisant le chemin de ce dossier à partir d'un fichier "bibli.conf", et où il y avait également un dossier où déposer les fichiers que nous devions créer, la commande suivante dans le shell devrait générer "la bibliothèque" :

```
bibli.py bibli.conf
```

### La Classe Trier :

Elle prend en argument un dossier et crée une liste pour chaque type de fichiers contenu dans le dossier, i.e. , une liste avec tous les fichiers pdf , une liste avec tous les fichiers epub, une liste avec les fichiers zip et une liste avec le reste.
Dans ce projet, les fichiers zip et les autres types de fichiers autre que les pdf et les epubs ne sont pas traités.

### La Classe PDF :

Elle extrait le titre, le nombre de pages, le nom de l'auteur, le langage et le table de matière du fichier pdf donné en argument.
Elle contient aussi une fonction toc qui permet d'obtenir la table des matières d'un fichier pdf. Il est sous forme : [ [str], [str], ... ].

### La Classe Epub :

Elle extrait le titre, le nombre de pages, le nom de l'auteur, le langage et le table de matière du fichier epub donne en argument.
Elle contient aussi une focntion toc qui permet d'obtenir la table des matières d'un fichier pdf. Il est sous forme str.

### La Classe Livres :

Elle génère une liste contenant le titre, l'auteur et le langage de chaque livre sous la forme : [ [titre,auteur,langage,nom du fichier], [titre,auteur,langage,nom du fichier] , etc....].
 
### La Classe Rapport :

Cette classe génère la liste des auteurs (au format texte, PDF et epub) contenant pour chacun d’eux les titres de ses livres et le nom des fichiers associés, i.e. :
 - 3 documents contenant une liste de la forme : [ [auteur, (livre1,nom du fichier,livre2,nom du fichier...)] , [auteur, (livre1,nom du fichier,livre2,nom du fichier...)] , ... ].

Elle génère aussi la liste des ouvrages (au format texte, PDF et epub) qui contient pour chaque livre son titre, son auteur, la langue et le nom du fichier correspondant, i.e. :
 - 3 autres documents contenant une liste de la forme : [ [titre,auteur,langage,nom du fichier], [titre,auteur,langage,nom du fichier] , ....].

Elle crée aussi 3 documents(pdf,epub,txt) pour CHACUN des fichiers contenu dans le dossier donné en argument, et contenant la table des matières du fichier.

Cette classe contient 3 fonctions :

##### La fonction write(): 

Elle crée la liste des auteurs et la liste des ouvrages en format txt et ensuite elle convertie chaque fichier txt en format pdf et en epub.
Elle prend en argument le chemin du dossier dans lequel on veut créer ces 6 documents.
 
##### La fonction ToC() :
Elle extrait la table des matières de chaque livres dans le dossier donné en argument au format txt, pdf et epub.
Elle prend comme argument le chemin du dossier dans lequel on veut créer ces documents.
 
##### La fonction Maj() :

Elle met à jour les rapports précédemment générés, en tenant compte de l’état présent de la bibliothèque : générer les rapports des nouveaux livres et supprimer les rapports des livres disparus.

Chaque exécution d’une mise à jour consigne les opérations réalisées (créations et suppression) dans un fichier de log.
