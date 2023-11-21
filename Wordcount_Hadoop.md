**Sommaire**

[TOC]


# Map-reduce, avec Hadoop

Étant donnée l'installation précédente, nous allons exploiter le parallélisme de votre processeur, souvent constitué de 4 cœurs, et donc susceptible de lancer 4 instructions en parallèle. Parmi ces 4 cœurs, nous n'en exploiterons que 3 (1 pour le _Namenode_ et 2 pour les _Datanodes_), le dernier cœur étant à disposition de votre machine pour toutes les autres tâches.

Deux commandes pour commencer :

1. La commande 
```bash
/usr/local/hadoop/bin/hdfs namenode -format
```
formate le disque dur hdfs. A ne faire que la première fois que vous rentrez dans le l_Namenode_ 

2. La commande
```bash
export JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
```
si vous disposez d'un processeur _amd_, ou la commande
```bash
export JAVA_HOME="/usr/lib/jvm/java-8-openjdk-arm64"
```
si vous disposez d'un processeur _intel_ (plus rare, mais utilisé par Apple dans ses derniers modèles).

---
## Lancement du _daemon_ **Hadoop**

La première chose à faire sur le _Terminal_ connecté au `hadoop-master` est de lancer les _daemon_ **Hadoop** :
```bash
./start-hadoop.sh
```
Le résultat de l'exécution de ce script ressemblera à :
```bash
Starting Namenodes on [hadoop-master]
hadoop-master: Warning: Permanently added 'hadoop-master,172.18.0.4' (ECDSA) to the list of known hosts.
hadoop-master: starting Namenode, logging to /usr/local/hadoop/logs/hadoop-root-Namenode-hadoop-master.out
hadoop-slave2: Warning: Permanently added 'hadoop-slave2,172.18.0.2' (ECDSA) to the list of known hosts.
hadoop-slave1: Warning: Permanently added 'hadoop-slave1,172.18.0.3' (ECDSA) to the list of known hosts.
hadoop-slave2: starting datanode, logging to /usr/local/hadoop/logs/hadoop-root-datanode-hadoop-slave2.out
hadoop-slave1: starting datanode, logging to /usr/local/hadoop/logs/hadoop-root-datanode-hadoop-slave1.out
Starting secondary Namenodes [0.0.0.0]
0.0.0.0: starting secondaryNamenode, logging to /usr/local/hadoop/logs/hadoop-root-secondaryNamenode-hadoop-master.out

starting yarn daemons
starting resourcemanager, logging to /usr/local/hadoop/logs/yarn--resourcemanager-hadoop-master.out
hadoop-slave1: Warning: Permanently added 'hadoop-slave1,172.18.0.3' (ECDSA) to the list of known hosts.
hadoop-slave2: Warning: Permanently added 'hadoop-slave2,172.18.0.2' (ECDSA) to the list of known hosts.
hadoop-slave1: starting nodemanager, logging to /usr/local/hadoop/logs/yarn-root-nodemanager-hadoop-slave1.out
hadoop-slave2: starting nodemanager, logging to /usr/local/hadoop/logs/yarn-root-nodemanager-hadoop-slave2.out
```


---
## Préparation des fichiers pour _wordcount_

> **Remarque importante** Le _Terminal_ pointe sur un système _Linux_ qui a son propre mode de stockage de fichier (appelé _ext3_). Il est alors possible de créer des dossiers, de déposer des fichiers, de les effacer... avec les commandes _Linux_ traditionnelles (```mkdir```, ```rm```...). Notons qu'il n'existe pas d'éditeur de texte intégré au container que nous venons d'installer (pour écrire les scripts _Python_), donc nous aurons recours à une astuce décrite ci-dessous.    
> C'est sur cet espace que nous stockerons les scripts _Python map-reduce_ qui seront exécutés par **Hadoop**. Par contre, les fichiers volumineux, ceux pour lesquels nous déploierons des algorithmes de traitement, seront stockés sur une partie de votre disque dur gérée par _HDFS_ (_Hadoop Distributed File System_). À l'aide de commandes commençant par _"`hadoop fs -` + commande"_, il est possible de créer des dossiers sur _HDFS_, de copier des fichiers depuis _Linux_ vers _HDFS_, et de rapatrier des fichiers depuis _HDFS_ vers Linux.  

Laissez-vous guider...

  - Depuis le _Terminal_, créez un dossier _wordcount_ et déplacez-vous dedans
```bash
mkdir wordcount
cd wordcount
```    
  - Téléchargez depuis internet le livre _dracula_ à l'aide de la commande
```bash
wget http://www.textfiles.com/etext/FICTION/dracula
```   
  - Versez ce fichier volumineux sur l'espace HDFS (après avoir créé un dossier pour le recevoir)
```bash
hadoop fs -mkdir -p input
hadoop fs -put dracula input
```
   Vérifiez que le fichier a bien été déposé:
```bash
hadoop fs -ls input
```
   ce qui donnera quelque chose comme:
```bash
Found 1 items
-rw-r--r--   2 root supergroup     844505 2020-10-16 05:02 input/dracula
```    
  - Supprimer le fichier _dracula_ de votre espace _Linux_ (on n'en a plus besoin!)
```bash
rm dracula
```     

Il faut maintenant rapatrier, sur notre espace Linux, les scripts _mapper.py_ et _reducer.py_ que nous avons manipulés durant la première partie de ce TP. Pour cela, il faut ouvrir un **second _Terminal_** (laissez le premier ouvert, il va nous resservir!), et vous déplacer dans le dossier de travail qui contient les scripts _mapper.py_ et _reducer.py_, modifiés par vos soins durant la première partie. La commande suivante permet de copier ces 2 fichiers vers l'espace Linux, dans le dossier _wordcount_
```bash
docker cp mapper.py hadoop-master:/root/wordcount
docker cp reducer.py hadoop-master:/root/wordcount
``` 
Retenez la syntaxe, car elle vous sera utile plus tard, pour rapatrier les nouveaux scripts _Python_ que vous aurez développés.

Revenez alors vers le **premier _Terminal_** (ne fermez pas le second, il sera utile plus tard), et vérifiez avec la commande ```ls``` que les 2 fichiers sont bien présents. Il faut maintenant 

 - rendre ces 2 scripts exécutables:
```bash
chmod +x mapper.py
chmod +x reducer.py
```
  Vérifiez, avec la commande `cat mapper.py`, que la première ligne du fichier est bien la suivante :
```bash 
#!/usr/bin/env python3
```   
  Si non, alors corrigez le fichier en conséquence!

 - Pour les utilisateurs de _Windows_ uniquement : il faut aussi convertir les caractères de saut de lignes, qui sont différents entre _Windows_ et _Linux_. Pour chaque fichier texte (_p. ex._, _fichier.py_) que vous rapatrierez depuis votre machine sur le compte _Linux_, il conviendra de lancer:
```bash
dos2unix fichier.py
```
  Il faudra appliquer ce protocole aux fichiers _mapper.py_ et _reducer.py_, à chaque fois que vous les aurez modifiés sous _Windows_.

Souvenez-vous de cette manip., car il faudra aussi la mettre en place sur vos nouveaux scripts.

Ça y est, nous sommes prêts à lancer notre premier script _map-reduce_ sous **Hadoop**!



---
## _Wordcount_ avec **Hadoop**

À partir du premier _Terminal_, nous allons donc lancer les scripts permettant de compter le nombre de mots sur le fichier du livre _dracula_.

- Tout d'abord, stockez le lien vers la librairie permettant de programmer avec _Python_ dans une variable système :
```bash
export STREAMINGJAR='/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.2.jar'
```    
Je vous rappelle que _**Hadoop** map-reduce_ fonctionne avec le langage **Java** ; il faut donc utiliser une bibliothèque capable de transformer des instructions _Python_ en instruction **Java**. C'est le rôle de cette bibliothèque _hadoop-streaming-3.2.2.jar_ (on appelle cela un _wrapper_).    
  
- Ensuite, lancez le _job_ **Hadoop** avec l'instruction suivante (copiez tout le bloc d'instructions et collez-le dans le _Terminal_):
```bash
hadoop jar $STREAMINGJAR -files mapper.py,reducer.py \
  -mapper mapper.py -reducer reducer.py \
  -input input/dracula -output sortie
``` 
L'option `-files` permet de copier les fichiers nécessaires pour qu'ils soit exécutés sur tous les nœuds du cluster.


Si jamais la commande ne fonctionnait pas correctement, vous pouvez essayer celle-ci:
```bash
hadoop jar $STREAMINGJAR -files /root/wordcount/mapper.py,/root/wordcount/reducer.py \
  -mapper "python mapper.py" -reducer "python reducer.py" \
  -input input/dracula -output sortie
```

Le résultat du comptage de mots est stocké dans le dossier _sortie_ sous _HDFS_. Vous pouvez voir son contenu en lançant la commande:
```bash
hadoop fs -ls sortie/
```
qui donnera quelque chose comme
```bash
Found 2 items
-rw-r--r--   2 root supergroup          0 2020-10-16 06:58 sortie/_SUCCESS
-rw-r--r--   2 root supergroup         25 2020-10-16 06:58 sortie/part-00000
```

Le premier fichier _\_SUCCESS_ est un fichier vide (0 octet!), dont la simple présence indique que le _job_ s'est terminé avec succès. Le second fichier _part-00000_ contient le résultat de l'algorithme. Vous pouvez visualiser les dernières lignes du fichier avec la commande :
```bash
hadoop fs -tail sortie/part-00000
```
ou voir tout le fichier avec la commande :
```bash
hadoop fs -cat sortie/part-00000
```
Le résultat devrait être exactement le même que lors de la première partie du TP.

*Remarque - N'oubliez pas!* : Entre 2 exécutions, il faut soit utiliser un nouveau nom pour le dossier _sortie_, soit le supprimer de la manière suivante :
```bash
hadoop fs -rm -r -f sortie
``` 

La présence d'un seul fichier ```part-0000x```  montre qu'un seul nœud a été utilisé pour le _reducer_ (le nombre de nœuds est estimé par le _Namenode_). Il est possible de forcer le nombre de _reducer_ :
```bash
hadoop jar $STREAMINGJAR -D mapred.reduce.tasks=2 \
  -files mapper.py,reducer.py \
  -input input/dracula -output sortie \
  -mapper mapper.py -reducer reducer.py \
```
La commande :
```bash
hadoop fs -ls sortie/
```
donnera alors :
```bash
Found 3 items
-rw-r--r--   2 root supergroup          0 2020-10-17 15:24 sortie/_SUCCESS
-rw-r--r--   2 root supergroup     117444 2020-10-17 15:24 sortie/part-00000
-rw-r--r--   2 root supergroup     118967 2020-10-17 15:24 sortie/part-00001
```

---
## Monitoring du cluster et des _jobs_

**Hadoop** offre plusieurs interfaces web pour pouvoir observer le comportement de ses différentes composantes. Vous pouvez afficher ces pages en local sur votre machine grâce à l'option _-p_ de la commande `docker run`. 
 
- Le **port 9870** permet d'afficher les informations de votre _Namenode_.      
- Le **port 8088** permet d'afficher les informations du _resource manager_ (appelé _Yarn_) et visualiser le comportement des différents jobs.

Une fois votre cluster lancé et prêt à l'emploi, utilisez votre navigateur préféré pour observer la page [http://localhost:9870](http://localhost:9870). _Attention_ : lors de l'installation, certains étudiants auront du supprimer le _mapping_ de ce port, ils ne leur sera donc pas possible de visualiser la page, semblable à :

![interface 9870](figures/interface9870.png)

Prenez le temps de naviguer dans les menus et d'observer les informations indiquées.

Vous pouvez également visualiser l'avancement et les résultats de vos _jobs_ (_map-reduce_ ou autre) en allant à l'adresse [http://localhost:8088](http://localhost:8088). Prenez le temps là-aussi de naviguer dans les menus et d'observer les informations indiquées.
