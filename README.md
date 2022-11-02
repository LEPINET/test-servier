# test-servier

# Constitution du projet

    |── run.py
    |── config.py
    |── data
    |──── graph
    |──── processed
    |──── source
    |── src
    |──── graph_generator.py
    |──── processing.py
    |──── utils.py
    |── sql
    |──── requete1
    |──── requete2
    |── tests

La première étape de préparation des données vérifie les colonnes requises des fichiers csv ainsi que convertit les fichier json en csv pour une utilisation ultérieure.
La fonction `process_files`permet cette transformation en appelant les différentes fonctions et prends les fichiers sources contenus dans `data/source` et met les fichiers transformer dans le dossier `data/processed`.
`process_json` transforme les fichiers json en csv et en vérifie les colonnes.
`process_csv` vérifie les colonnes des fichiers csv.

La seconde étape permettant la construction du graph se fait à l'aide de la fonction `generate_graph`.
Les différentes fonctions appelées dans `graph_generator.py` permettent de retrouver les différents médicaments et de les lier avec les différentes sources possibles à savoir `pubmed` et `clinical_trials`.
`find_occurence` retrouve les références faites d'un médicaments dans un fichier csv.
Les autres fonctions permettent de construire les éléments du dictionnaires finale.

Un élément du dictionnaire finale ressemble à ceci :

 "atropine": {
        "journal": {
            "The journal of maternal-fetal & neonatal medicine": [
                "01/03/2020"
            ]
        },
        "clinical_trials": [],
        "pubmed": [
            {
                "title": "comparison of pressure betamethasone release, phonophoresis and dry needling in treatment of latent myofascial trigger point of upper trapezius atropine muscle.",
                "date": "01/03/2020"
            }
        ]
    }

Les éléments du dictionnaire finale sont rangé par nom du médicaments ou `drug`. Ce dictionnaire contient lui-même trois éléments à savoir les deux types de sources ainsi que `journal` qui répertorie les journaux et leur date de parution faisant référence au médicaments.
Les type de sources contiennent une liste d'élément donnant le titre et la date de l'article.

# Exécution

- Activation de l'environnement virtuel
- Installation des librairies en tapant `make requirements`
- Exécution du pipeline avec : `make run`


Le fichier `find_journal.py` si lancer donne un fichier `result_max_journal.txt` contenant un tuple donnant le journal ayant le plus de référence pour un médicament ainsi que le nombre de médicaments différents. C'est ici `pharmacologie` qui cite le plus de médicaments différents, 2.

# Adaptation du code pour une plus grande quantité de données

Afin de traiter une grand volumétrie de données, pour des fichiers de grande taille, un découpage de ceux ci peut se faire à l'aide de pandas ou par une autre librarie en ajoutant un module de pré-traitement des gros fichiers.

Pour un grand nombre de fichiers, une parallélisation s'impose en créant plusieurs threads.
Si la taille des fichier est faible, nous pouvons aussi envisager une fusion de ces derniers.


# Les requêtes SQL demandées se situe dans le dossier SQL


