**Sommaire**

[[_TOC_]]

# TP Hadoop

Ce TP fait suite au cours sur le _framework_ libre et open source appelé [__Hadoop__](https://Hadoop.apache.org), développé et maintenu par la [Fondation Apache](https://www.apache.org).

> *Remarque* : Pour ce TP, vous devez savoir ouvrir un _Terminal_ sur votre machine, quelque soit le système d'exploitation (_Windows_, _Linux_, ou _Mac OS X_). Sous _Windows 10_, vous pourrez utiliser le programme _Windows powershell_ qui est très similaires au _Terminal_ de _Linux_ et de _Mac OS X_. Vous devez aussi savoir naviguer dans vos dossiers à l'aide de la commande ```cd```. Typiquement :
```shell
cd c:\Users\elossmani\TP_Hadoop # Windows
cd ~\TP_Hadoop                 # Mac, linux
```
Si vous souhaitez remonter d'un niveau dans la hiérarchie des dossiers: ```cd ..```. Des tutos vidéo existent pour décoruvrir les comandes de bases (identiques à celles que l'on retrouve sur les systèmes _Linux_).


---
## Installer **git** pour Windows (si requis)

Avant de commencer, il faut vérifier que **git** (un gestionnaire de version de fichier) est bien installé sur votre machine. **git** est disponible par défaut sur les machines *Mac OS X* et *Linux* et *Windows 10*. Pour vérifier, lancez la commande suivante dans un _Terminal_
```shell
git --version
```
S'il est absent, alors installez-le grâce à ce lien : [git-scm](https://git-scm.com/download/win). Lors de l'installation, validez les choix par défaut qui vous sont proposés.



---
## TP partie 1 - _wordcount_ _map-reduce_ en local

Suivez  les consignes permettant d'exécuter l'algorithme _map-reduce_ de comptage de mots en local, sur le fichier contenant un livre (_Dracula_) au format texte : 
> [Wordcount_Local.md](./Wordcount_Local.md)


---
## TP partie 2 - _map-reduce_ avec Hadoop

Pour installer **Hadoop** sur votre machine (à l'aide de *Docker*), suivez les consignes du fichier : 
> [Install_Docker_Hadoop.md](./Install_Docker_Hadoop.md)

Suivez ensuite les consignes permettant de lancer le comptage de mots en tant que _job map-reduce_ : 
> [Wordcount_Hadoop.md](./Wordcount_Hadoop.md)

Enfin, répondez aux exercices de cet énoncé : 
> [Enonce_TP_Hadoop.md](./Enonce_TP_Hadoop.md)


