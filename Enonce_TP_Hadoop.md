**Sommaire**

[[_TOC_]]

# Travaux pratiques sous **Hadoop**

**Objectif du travail** : recueillir des informations et calculer des statistiques sur des résultats de ventes stockés dans le fichier _purchases.txt_. 


---
## Préparation et conseils

Dans le _shell_ du _Namenode_, créez un dossier, déplacez le fichier _purchases.txt_ dans ce dossier et déplacez-vous dedans (à partir du premier _Terminal_) :
```shell
cd .. 
mkdir ventes
mv purchases.txt ventes
cd ventes
```
La première commande permet de remonter dans l'arborescence des dossiers d'un niveau (nous étions dans le répertoire _wordcount_). Pour observer le contenu du fichier :
```shell
more purchases.txt
```

La commande `more` affiche  le contenu du fichier page par page. La barre d'espace permet de voir la page suivante. Pour stopper la visualisation du contenu du fichier, tapez `q`. Ainsi, vous pouvez constater que le fichier est organisé en 6 colonnes :

 - date (format `YYYY-MM-DD`);    
 - heure (format `hh:mm`);    
 - ville d'achat;    
 - catégorie de l'achat (parmi _Book_, _Men's Clothing_, _DVDs_...);    
 - somme dépensée par le client;    
 - moyen de paiement (parmi _Amex_, _Cash_, _MasterCard_...).

Les colonnes sont séparées par une tabulation. Ce caractère  est codé par _\t_ en _Python_. Exemple : `print("avant\tapres")` permet d'obtenir l'impression de la chaîne "_avant&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;apres_".

La commande _Linux_ `wc -l purchases.txt` permet d'obtenir le nombre de lignes du fichier (soit 4 138 476 lignes!). Ce fichier est sans doute trop volumineux pour régler vos algorithmes (le temps de debug en serait largement augmenté). Aussi, il est conseillé de travailler avec un extrait du fichier :
```shell
cat purchases.txt | head -n 100 > purchases_extrait100.txt
```
Cette commande extrait les 100 premières lignes du fichier et les stocke dans un fichier appelé _purchases_extrait100.txt_. N'oubliez cependant pas de vérifier vos scripts définitifs avec le fichier original.

Pensez à envoyer ces deux fichiers sur HDFS, dans le dossier _input_ :
```shell
hadoop fs -put purchases.txt input
hadoop fs -put purchases_extrait100.txt input
```

**Remarque** : Il n'est pas possible de programmer directement dans le _shell_ du _Namenode_, car celui-ci ne dispose pas d'éditeur de texte. La solution consiste à 

 1. programmez vos scripts _map_ et _reduce_ avec votre IDE préférée (et pourquoi pas _Spyder_);    
 1. stockez vos fichiers (appelés _vente\_map.py_ et _vente\_reduce.py_) dans un dossier _vente_ que vous aurez créé sur votre machine (à côté du répertoire _wordcount_ de la première partie du TP ?);    
 1. stockez vos fichiers (appelés _vente\_map.py_ et _vente\_reduce.py_) dans un dossier _vente_ que vous aurez créé sur votre machine (à côté du répertoire _wordcount_ de la première partie du TP ?);    
 1. envoyez vos 2 fichiers vers le _Namenode_ :
 ```shell
 docker cp vente_map.py hadoop-master:/root/ventes
 docker cp vente_reduce.py hadoop-master:/root/ventes
 ```
 
Avant de lancer le _job_ que vous aurez prévu dans les fichiers _vente_map.py_ et _vente_reduce.py_
```shell
hadoop jar $STREAMINGJAR -input input/purchases_extrait100.txt -output sortie -mapper vente_map.py -reducer vente_reduce.py -file vente_map.py -file vente_reduce.py
``` 
dans le _shell_ du _Namenode_, pensez à rendre vos scripts exécutables :
```shell
chmod +x vente_map.py
chmod +x vente_reduce.py
```
Vérifiez, avec la commande `more vente_map.py`, que la première ligne du fichier est bien la suivante :
```shell
#!/usr/bin/env python3
```   
Si non, alors corrigez le fichier en conséquence!    
Et si vous utilisez _Windows_, pensez également à convertir les fins de ligne de ces 2 fichiers avec `dos2unix`.

Vous êtes maintenant équipés pour développer les scripts _map-reduce_ permettant de répondre aux questions suivantes.

---
## Exercice 2 - Questionner le fichier de ventes

Voici une liste de questions que vous pouvez aborder dans l'ordre (ou non!):

 1. Quel est le nombre d'achats effectués pour chaque catégorie d'achat ?    
 1. Quelle est la somme totale dépensée pour chaque catégorie d'achat ?   
 1. Quelle somme est dépensée  dans la ville de _San Francisco_ dans chaque moyen de paiement ?
 1. Dans quelle ville la catégorie _Women's Clothing_ a permis de générer le plus d'argent _Cash_ ?
 1. À quelle heure les clients dépensent-ils le plus ?

Il est conseillé de développer un couple de fichiers différent pour chaque question (pour garder trace de vos algorithmes).
