# SAE52

Docker version : Docker version 18.09.1, build 4c52b90

Disclaimer : le logiciel python de log ne fonctionne que sur alpine

![Alt1](images/Dashboard.png?raw=true "Rendu final")

## Objectifs

1. Produire un document de synthèse en Markdown présentant les solutions libres existantes de
collecte, centralisation et présentation de logs. Vous donnerez leurs points-clés (features, communauté
associée, etc.) et leurs avantages et inconvénients respectifs. Vous vous intéresserez notamment aux
possibilités de centralisation (collecte des logs issus de plusieurs conteneurs/machines), à la facilité
d’utilisation et d’installation, et aux possibilités offertes par les "dashboard".

2. Produire un Dockerfile qui met un oeuvre une situation simple de collecte de logs, basée sur une
des solutions existantes. Le lancement du (des ?) conteneur(s) doit permettre de se faire une idée des
possibilités, via une doc associée (rédigée en Markdown).

## Réalisation

![Alt2](images/Functionning.png?raw=true "Explication du fonctionnement")

## Objectif 1

## Objectif 2

Pour la mise en oeuvre du Dockerfile, nous avons choisi d'utiliser docker-compose pour démarrer nos différents containers : Grafana, Prometheus et logger.

Afin de lancer le projet, il suffit de faire ceci dans la racine du projet :

> docker-compose up -d

Ensuite, il ne reste plus que à se connecter à Grafana sur une des deux addresses suivantes :

> localhost:3000
> IP_de_votre_VM:3000

Utiliser localhost dans le cas ou vous lancer le projet sur le docker de votre machine principal et la deuxième solution si docker est dans une VM sur votre système.

Vous devez vous connecter avec les identidiants suivants :

> admin:admin

Vous pouvez passer l'étape de changement de mot de passe et directement passer sur le setup des datasources du `JSON API`.

Vous devez rentrer les paramètres comme ceci :

![Alt3](images/JSON_API.png?raw=true "Datasource")

La datasource donnera mais une erreur mais aucun soucis, ça fonctionne ;)

Une fois ceci réglé, il faut importer le dashboard avec le fichier suivant :

> ![Dashboard d'importation](Dashboard_export.json)

Et normalement tout fonctionne, vous pouvez voir les metrics sur le dashboard `Node1`


