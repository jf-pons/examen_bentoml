# Examen BentoML
Ce projet contient comme demandé :
- Le présent fichier "README.md" permettant d'expliquer comment exécuter les tests
- L'archive de l'image de l'API
- Des fichiers pour les tests unitaires

## Comment utiliser le projet
Il y a deux approches proposées ici:
- La première consiste à respecter les consigne de l'examen avec l'utilisation d'une archive
- La seconde est un essai fonctionnel d'utilisation d'un Makefile pour générer l'image et exécuter les tests

Les deux approches sont détaillées ci-dessous.

### Version 1: Utilisation d'une archive
Dans l'examen, on demande d'utiliser une archive `.tar` contenant l'image docker de l'API puis d'exécuter les tests.
Les commandes pour réaliser cela sont les suivantes :
```bash
docker image load -i bento_image.tar
docker run docker run -d --rm -p 3000:3000 pons_student_admission:2s2uxbuby2tuqcs6
pipenv install --dev
pipenv run python -m pytest tests
```


### Version 2: Utilisation d'un makefile
>**Note :** Dans cette version, j'ai fait le choix d'utiliser [pipenv](https://pipenv.pypa.io/en/latest/) pour la gestion des packages Python. Il est donc supposer que celui-ci est installé.
Pour récupérer les données, entraîner le modèle, générer le Bento, créer l'image et lancer les tests, il suffit de lancer la commande suivante:
```bash
make all
```

Pour nettoyer l'ensemble des fichiers et objets générés lors de l'exécution de la commande précédente, il suffit de lancer la commande suivante:
```bash
make clean
```

