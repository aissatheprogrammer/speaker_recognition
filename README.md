# Speaker_recognition

L'objectif de cette application est de mettre en place un système d'identification par reconnaissance vocale. 
L'idée est d'empêcher l'usurpation d'identité (accès à des informations confidentielles, des lieux à accès restreints...) avec une méthode non intrusive et ergonomique.

Pour illustrer ce système d'identification vocale, 3 classes sont distinguées :
- "aissa" : désigne une personne dont l'accès est autorisé.
- "marouan" : désigne une autre personne dont l'accès est autorisé.
- "autre" : désigne tout autre personne dont l'accès n'est pas autorisé.

A partir d'un enregistrement vocal, le système est capable de déterminer à quelle classe il est associé et ainsi décider d'accorder l'accès ou non.

## Améliorations possibles

Des améliorations sont possibles pour rendre le système encore plus fiable et plus ergonomique :
- Le modèle de classification utilisé est relativement simple (régression logistique) et donne des résultats globaux peu satisfaisants (71%). En utilisant un modèle plus complexe, on peut espérer obtenir des meilleures résultats.   
Avec des meilleurs résultats, on diminue le risque d'usurpation d'identité et on améliore l'ergonomie du dispositif (puisque les personnes autorisées auront moins besoin de répéter pour être détectés correctement).
- L'identification vocale est l'unique couche de sécurité disponible. On peut ajouter une autre couche de sécurité avec une passphrase.
- L'interface Web nécessite une remise à niveau pour améliorer sa lisibilité.

Pas implémenté
- La méthode pour s'identifier sur l'application nécessite d'avoir un fichier wav déjà enregistré ou d'enregistrer un vocal via un voice recorder et charger le fichier dans l'application.
Il est préférable de pouvoir enregistrer directement l'audio via l'application (plus ergonomique).

### Compréhension des métriques importantes pour ce cas d'usage
Recall pour les classes "Aissa" et "Marouan". On peut améliorer le recall pour la classe Aissa afin que les personnes autorisées aient moins besoin de répéter pour pouvoir s'identifier (ergonomie ++).

Recall pour la classe "autre" (c'est-à-dire les personnes non autorisées) pour fiabiliser davantage le système et détecter toutes les personnes non autorisées.

Précision pour la classe "autre".
Eviter l'usurpation d'identité.

Pour les classes "Aissa" et "Marouan", on porte une attention particulière au recall.

Pour la classe "autre", on se concentre sur le f1 score.



## Solutions d'amélioration envisagées

### Pour l'amélioration des métriques
Le modèle actuel utilisé est une régression logistique.

1ère piste :  
En utilisant un modèle plus complexe tel que RandomForest + une optimisation des hyper-paramètres, on peut espérer obtenir des meilleurs résultats. 

2ème piste :  
Considérant que la représentation de l'audio en spectrogramme se rapproche de celle d'une image, on peut émettre l'hypothèse qu'un algorithme de deep learning avec une architecture CNN permettra d'avoir une meilleure extraction des caractéristiques du son et donc une meilleure discrimination (et potentiellement une amélioration des métriques de classification).

3ème piste :  
Comme le deep learning nécessite en général une grande quantité de données d'entrainement (ce que nous ne possédons pas) pour extraire les caractéristiques discriminantes, il parait judicieux de faire du transfer learning en utilisant des algorithmes déjà entrainés sur un grand volume de données audio. En effet, ces algorithmes déjà entrainés sont capables d'extraire les caractéristiques haut niveau d'un audio, il suffira d'ajouter des couches externes à entrainer avec les audios enregistrés pour les 3 classes "aissa", "marouan" et "autre".

D'après ce papier de recherche (https://www.mdpi.com/2224-2708/10/4/72), VGGish et YAMNet sont les algorithmes donnant les meilleurs résultats pour de la classification d'audios. VGGish est très légèrement meilleur, mais YAMNet semble être plus utilisé (100k vs 10k téléchargements sur tensorflow hub) et il semble y avoir davantage de documentation montrant comment l'utiliser. C'est pourquoi il est choisi pour le transfer learning.

On considére que l'amélioration est significative si les métriques augmentent de 5%.

Charge de travail estimée : 3 jours
Charge effective : 4 jours


### Pour l'ajout d'une couche de sécurité
Définir une passphrase à prononcer pour pouvoir s'identifier et intégrer un module de STT dans l'application qui permet de détecter la passphrase.

Charge de travail estimée : 1/2 jour
Charge effective : 1/2 jour


### Pour l'amélioration de l'interface
Améliorer le CSS du front end (avec Tailwind)

Non implémenté  
Utiliser un outil javascript pour enregistrer directement un audio sur l'application.
L'interface javascript MediaRecorder permet de faire cela assez facilement. Il faudra cependant récupérer le fichier audio enregistré et l'envoyer au serveur via une requête ajax.

Charge de travail estimée : 1/2 jour
Charge effective : 1/2 jour
