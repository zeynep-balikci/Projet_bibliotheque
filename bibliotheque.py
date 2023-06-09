#!/bin/env python3
import glob
import os 
from os import path
from PyPDF2 import PdfReader # pour pouvoir l'utiliser : pip install PyPDF2
import ebooklib # pour pouvoir l'utiliser : pip install ebooklib
from ebooklib import epub 
from bs4 import BeautifulSoup #pour convertir HTML en STR
import fitz  # pour pouvoir l'utiliser : pip install PyMuPDF
from langdetect import detect # pour pouvoir l'utiliser : pip install langdetect
import aspose.words as aw # pour pouvoir l'utiliser : pip install aspose.words
import logging

class Trier():
    """
    Cette classe trie les fichiers du dossier donné en argument. Il crée une liste dans laquelle se trouve le chemin d'accès de tous les fichiers pdf du dossier,
    ainsi qu'une autre liste dans laquelle se trouve le chemin d'accès de tous les fichiers epub du dossier.
    """
    def __init__(self,dossier):
        self.dossier=glob.glob(os.path.join(dossier,"*"))
        self.DocumentsPDF=[]
        self.DocumentsEpub=[]
        self.DocumentsZip=[]
        self.DocumentsAutres=[]
        for doc in self.dossier:
            nature=(os.path.splitext(doc)[1])
            if nature =='.pdf':
                self.DocumentsPDF.append(doc)
            if nature =='.epub':
                self.DocumentsEpub.append(doc)
            if nature =='.zip':
                self.DocumentsZip.append(doc)
            if nature == '':
                self.DocumentsAutres.append(doc)
    
    def __str__(self):
        return f"Il y a {len(self.DocumentsPDF)+len(self.DocumentsEpub)+len(self.DocumentsZip)+len(self.DocumentsAutres)} fichiers dans ce dossier"
    def __repr__(self):
        return f"Il y a {len(self.DocumentsPDF)+len(self.DocumentsEpub)+len(self.DocumentsZip)+len(self.DocumentsAutres)} fichiers dans ce dossier"

class PDF():
    """
    Cette classe extrait le titre,le nombre de pages, le nom/prénom de l'auteur, la langue et le table de matière du fichier pdf donné en argument.
    """
    def __init__(self,chemin_fichier):
        self.fichier= chemin_fichier
        livre = PdfReader(self.fichier)
        donnees = livre.getDocumentInfo()
        self.auteur = donnees.author if donnees.author else u'Inconnu'
        t = donnees.title if donnees.title else path.basename(self.fichier)
        self.titre=t.replace('"',"-")
        self.nom=path.basename(self.fichier)
        
        #Pour détecter la langue, on va utiliser le texte de la page 4, car pour certains fichiers pdf on ne pouvait pas détecter le nombre de pages ou le texte,
        #parce que certains fichiers pdf ne sont composé que d'images.
        try:
            self.pages= len(livre.pages)
        except :
            self.pages=0
        if self.pages>4:
            page = livre.pages[4]
            text = page.extract_text()
            try:
                self.langage=detect(text)
            except:
                self.langage='Inconnu'
        else :
            self.langage='Inconnu'
            
    def __str__(self):
        return f"{self.titre} de {self.auteur}"
    
    def __repr__(self):
        return f"{self.titre} de {self.auteur}"
    
    def toc(self):
        """ 
        Cette fonction nous permet d'obtenir la table des matières d'un fichier pdf. Il est sous forme : [ [str], [str], ...     ]
        """
        livre = fitz.open(self.fichier)
        return livre.get_toc()

class Epub():
    """
    Cette classe extrait le titre, le nom/prénom de l'auteur, la langue et la table de matières du fichier epub donné en argument.
    """
    def __init__(self,chemin_fichier):
        self.fichier=chemin_fichier
        livre = epub.read_epub(self.fichier)
        self.auteur=livre.get_metadata('DC', 'creator')[0][0]
        self.titre=livre.get_metadata('DC', 'title')[0][0]
        self.langage=livre.get_metadata('DC', 'language')[0][0]
        self.nom=path.basename(self.fichier)        
        livre = fitz.open(self.fichier)
        self.pages=livre.page_count
        
    def toc(self):
        """ 
        Cette fonction nous permet d'obtenir la table des matières d'un fichier epub. Il est sous forme de str.
        """
        book = epub.read_epub(self.fichier)
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_NAVIGATION:
                soup = BeautifulSoup(item.get_content(), features="xml")
        toc = soup.get_text()
        return toc.replace('\n\n\n\n',"")

    def __str__(self):
        return f"{self.titre} de {self.auteur}"
    
    def __repr__(self):
        return f"{self.titre} de {self.auteur}"

class Livres():
    """
    Cette classe crée une liste contenant le titre, l'auteur et la langue de chaque fichier de la liste de fichiers donnée en argument.
    La liste de fichiers est une liste des chemins des fichiers.
    La liste crée est de la forme :
    [   [titre,auteur,langue,nom du fichier] ,   [titre,auteur,langue,nom du fichier] , .... ]
    """
    def __init__(self,liste_fichiers):
        self.livres=[]
        self.liste_fichiers=liste_fichiers
        for fichier in self.liste_fichiers:
            nature=(os.path.splitext(fichier)[1])
            if nature =='.pdf':
                livre=PDF(fichier)
                self.livres.append([livre.titre,livre.auteur,livre.langage,livre.nom])
            if nature =='.epub':
                livre=Epub(fichier)
                self.livres.append([livre.titre,livre.auteur,livre.langage,livre.nom])
                
    def __str__(self):
        return "\n".join([str(c) for c in self.livres])
    
    def __repr__(self):
        return "\n".join([str(c) for c in self.livres])


class Rapport():
    """
    Cette classe crée 6 documents pour l'ensemble des fichier contenu dans le dossier donné en argument:
        3 documents (pdf,epub,txt) contenant le nom de chaque auteur, le titre de ses livres et le nom du fichier de ces livres :
        [   [auteur1, livre1, nom du fichier du livre1, livre2, nom du fichier du livre 2, ...]   ,    [auteur2, livre1, nom du fichier du livre1, ...]   ,   ... ]
        3 autres documents (pdf,epub,txt) contenant pour le titre de chaque livre, l'auteur, la langue et le nom du fichier :
        [   [titre, auteur, langue, nom du fichier],    [titre, auteur, langue, nom du fichier] , ....]
        
    Elle crée aussi 3 documents(pdf,epub,txt) pour CHACUN des fichiers contenu dans le dossier donné en argument, et contenant la table des matières du fichier.
    
    """
    def __init__(self, dossier):
        self.dossier=dossier
        self.livresPDF=Trier(self.dossier).DocumentsPDF # liste des chemins des livres pdf
        self.livresEpub=Trier(self.dossier).DocumentsEpub # liste des chemins des livres epub 
        self.rapport=Livres(self.livresEpub).livres # liste des livres : [ [titre,auteur,langue,nom du fichier] , [titre,auteur,langue,nom du fichier] , .... ]
        for livre in Livres(self.livresPDF).livres:
            self.rapport.append(livre)

        #pour obtenir la liste des auteurs et de ses livres :
        self.rapport2=[]
        self.auteurs=[]
        for livre in self.rapport:
            if livre[1] in self.auteurs:
                pass
            else :
                self.auteurs.append(livre[1])
                self.rapport2.append([livre[1]])
                
        for auteur in self.auteurs :
            for livre in self.rapport :
                if auteur == livre[1]:
                    self.rapport2[self.auteurs.index(auteur)].append(livre[0])
                    self.rapport2[self.auteurs.index(auteur)].append(livre[3])
        # self.rapport2 est de la forme : 
        # [ [auteur1, livre1, nom du fichier du livre1, livre2, nom du fichier du livre 2, ...] ,  [auteur2, livre1, nom du fichier du livre1, ...]   ,   ... ]

    def write(self,chemin_rapports):
        """
        Cette fonction permet de crée la liste des ouvrages et la liste des auteurs sous format txt, pdf et epub.
        Elle prend comme argument le chemin du dossier dans lequel on veut créer ces 6 documents.
        """
        ancien_repertoire = os.getcwd()
        os.chdir(chemin_rapports)
        
        # Création des fichiers txt:
        # La liste des ouvrages :
        with open("La liste des ouvrages.txt","w") as f :
            f.write("\nLivre 1 : \n Le titre : "+self.rapport[0][0])
        
        with open("La liste des ouvrages.txt","a+") as f :
            f.write("\n L'auteur : "+self.rapport[0][1])
            f.write("\n La langue : "+self.rapport[0][2])
            f.write("\n Le nom du fichier : "+self.rapport[0][3])
            for i in range(1,len (self.rapport)):
                f.write(f"\n\nLivre {i+1} : \n Le titre : {self.rapport[i][0]}")
                f.write("\n L'auteur : "+self.rapport[i][1])
                f.write("\n La langue : "+self.rapport[i][2])
                f.write("\n Le nom du fichier : "+self.rapport[i][3])
        # La liste des auteurs :
        with open("La liste des auteurs.txt","w") as f :
            f.write("Auteur 1 : "+self.rapport2[0][0])
            f.write("\n Ses livres :")
            for k in range (1,int((len(self.rapport2[0]))/2)+1):
                f.write(f"\n Livre {k} : {self.rapport2[0][2*k-1]} et le nom du fichier : {self.rapport2[0][2*k]} ")
        with open("La liste des auteurs.txt","a+") as f :
            for i in range(1,len(self.rapport2)):
                f.write(f"\n\nAuteur {i+1} : {self.rapport2[i][0]}")
                f.write("\n Ses livres :")
                for j in range (1,int((len(self.rapport2[i]))/2)+1): 
                    f.write(f"\n Livre {j} : {self.rapport2[i][2*j-1]} et le nom du fichier : {self.rapport2[i][2*j]} ")
               
        # conversion de la liste txt en pdf
        doc = aw.Document("La liste des ouvrages.txt")
        doc.save("La liste des ouvrages.pdf",aw.SaveFormat.PDF)
        doc = aw.Document("La liste des auteurs.txt")
        doc.save("La liste des auteurs.pdf",aw.SaveFormat.PDF)
        
        # conversion de la liste txt en epub
        doc = aw.Document("La liste des ouvrages.txt")
        doc.save("La liste des ouvrages.epub",aw.SaveFormat.EPUB)
        doc = aw.Document("La liste des auteurs.txt")
        doc.save("La liste des auteurs.epub",aw.SaveFormat.EPUB)
        os.chdir(ancien_repertoire)
        
    def ToC(self,chemin_rapports):
        """
        Cette fonction crée 3 documents (pdf,epub,txt) contenant la table des matières de chacun des fichiers contenu dans le dossier donné en argument.
        Elle prend comme argument le chemin du dossier dans lequel on veut créer ces documents.
        """
        ancien_repertoire = os.getcwd()
        os.chdir(chemin_rapports)
        for file in self.livresPDF:
            # Création du fichier txt:
            livre = PDF(file)
            toc= livre.toc()
            with open(f"La table des matières de {livre.nom[:-4]}.txt","w") as f :
                if len(toc)>1:    
                    f.write("\n"+str(toc[0]))
                    for i in range(1,len (toc)):
                        f.write(f"\n {str(toc[i])}")
                else :
                    f.write("Ce livre ne possède pas de table de matière")
            # conversion de la liste txt en pdf:           
            doc = aw.Document(f"La table des matières de {livre.nom[:-4]}.txt")
            doc.save(f"La table des matières de {livre.nom[:-4]}.pdf",aw.SaveFormat.PDF)
            # conversion de la liste txt en epub
            doc = aw.Document(f"La table des matières de {livre.nom[:-4]}.txt")
            doc.save(f"La table des matières de {livre.nom[:-4]}.epub",aw.SaveFormat.EPUB)
            
        for file in self.livresEpub:
            livre = Epub(file)
            toc= livre.toc()
            # Création du fichier txt:
            with open(f"La table des matières de {livre.nom[:-5]}.txt","w") as f :
                 f.write(toc)
            # conversion de la liste txt en pdf
            doc = aw.Document(f"La table des matières de {livre.nom[:-5]}.txt")
            doc.save(f"La table des matières de {livre.nom[:-5]}.pdf",aw.SaveFormat.PDF)
            # conversion de la liste txt en epub
            doc = aw.Document(f"La table des matières de {livre.nom[:-5]}.txt")
            doc.save(f"La table des matières de {livre.nom[:-5]}.epub",aw.SaveFormat.EPUB)
        os.chdir(ancien_repertoire)
            
    def MaJ(self,chemin_rapports) : #Mise à jour des rapports
        """
        Cette classe met à jour les rapports précédemment générés, en tenant compte de l’état présent de la bibliothèque : générer la nouvelle liste des ouvrages,
        la nouvelle liste des auteurs, et générer les fichiers contenant la tables des matières des nouvelles livres en plus de supprimer ceux des livres disparus.
        
        ELLE NE PEUT PAS MODIFIER LES RAPPORTS DES LIVRES QUI ONT ETE MODIFIES DEPUIS LA DERNIERE GENERATION (nous n'avons pas compris la demande)
        Chaque exécution d’une mise à jour consigne les opérations réalisées (créations, modifications et suppression) dans un fichier de log.
        Le fichier log est enregistré dans le dossier où se trouvre le fichier python exécuter.
        """     
        ancien_repertoire = os.getcwd()
        os.chdir(chemin_rapports)
        
        # On crée la liste des chemins des livres disparus:
        with open("La liste des ouvrages.txt","r") as f:
            lines=f.readlines()
        old_files=[]
        for i in range(1,int((len(lines))/6)+1):
            nom_fichier=lines[6*i-1]
            n=nom_fichier.replace(" Le nom du fichier : ","")
            old_files.append(self.dossier+"/"+n.replace("\n",""))
            
        # On crée la liste des chemins de TOUS les livres dans le dossier donné en argument en initialisation
        new_livresPDF=Trier(self.dossier).DocumentsPDF 
        new_livresEpub=Trier(self.dossier).DocumentsEpub
        new_files=new_livresPDF 
        for livre in new_livresEpub:
            new_files.append(livre)

        # On regénére les 6 fichiers (et on écrase les anciens) : la liste des ouvrages et la liste des auteurs 
        livresPDF_new=Trier(self.dossier).DocumentsPDF
        livresEpub_new=Trier(self.dossier).DocumentsEpub
        
        new_rapport=Livres(livresEpub_new).livres
        for livre in Livres(livresPDF_new).livres:
            new_rapport.append(livre)
        
        new_rapport2=[]
        auteurs=[]
        for livre in new_rapport:
            if livre[1] in auteurs:
                pass
            else :
                auteurs.append(livre[1])
                new_rapport2.append([livre[1]])    
        for auteur in auteurs :
            for livre in new_rapport :
                if auteur == livre[1]:
                    new_rapport2[auteurs.index(auteur)].append(livre[0])
                    new_rapport2[auteurs.index(auteur)].append(livre[3])
        
        self.rapport=new_rapport
        self.rapport2=new_rapport2
        self.write(chemin_rapports) 
        
        # Pour la crétion et supression des tables de matières
        files_added=[]
        files_deleted=[]
        
        for file in new_files:
            if file not in old_files:
                files_added.append(file)
        for file in old_files:
            if file not in new_files:
                files_deleted.append(file)

        livresPDF_to_create=[]
        livresEpub_to_create=[]
        for file in files_added:
            nature=(os.path.splitext(file)[1])
            if nature =='.pdf':
                livresPDF_to_create.append(file)
            if nature =='.epub':
                livresEpub_to_create.append(file)
        
        livresPDF_to_delete=[]
        livresEpub_to_delete=[]
        for file in files_deleted:
            nature=(os.path.splitext(file)[1])
            if nature =='.pdf':
                livresPDF_to_delete.append(file)
            if nature =='.epub':
                livresEpub_to_delete.append(file)
        
        for livre in livresEpub_to_delete:
            l=path.basename(livre[:-5])
            os.remove(f"La table des matières de {l}.txt")
            os.remove(f"La table des matières de {l}.pdf")
            os.remove(f"La table des matières de {l}.epub")
        for livre in livresPDF_to_delete:
            l=path.basename(livre[:-4])
            os.remove(f"La table des matières de {l}.txt")
            os.remove(f"La table des matières de {l}.pdf")
            os.remove(f"La table des matières de {l}.epub")
            
        self.livresPDF=livresPDF_to_create
        self.livresEpub=livresEpub_to_create
        self.ToC(chemin_rapports)
        
        # Création du fichier log :
        Log_Format = "%(levelname)s %(asctime)s - %(message)s"

        logging.basicConfig(filename = "Modifications.log",
                            filemode = "w",
                            format = Log_Format, 
                            level = logging.INFO)
        logger = logging.getLogger()

        l1 = "\n".join([str(c) for c in files_added])
        l2 = "\n".join([str(c) for c in files_deleted])
        logger.info("Les livres ajoutés sont :\n" + l1)
        logger.info("Les livres effacés sont :\n" + l2)
        # logging.shutdown() pour pouvoir effacé le fichier log
        os.chdir(ancien_repertoire)
