# PTS3-PTS4
Lisez ce document avant de vous lancer dans l'utilisation du git
## Se préparer à l'utilisation du git 
Avant de commencer à push, se munir de : 
* Git bash (à télécharger)
* pull le contenu du projet

## Introduction à git flow 
Il s’agit d’un ensemble de pratiques fonctionnant en branches sur git :
* **master** : branche contenant le produit en production (**les développeurs ne doivent jamais y écrire**)
* **develop** : branche contenant les fonctionnalités pour la prochaine version à mettre en production (**Les développeurs doivent éviter d'y écrire**)
* **feature** : branche utilisée pour stocker des sous branches qui seront nos features (fonctionnalités) à développer
* **release** : branche de préparation à la nouvelle version avec les fonctionnalités de develop et celles présentes dans master et correction des différents bugs rencontrés ;
Cette branche permet aux autres membres de l’équipe de développer des fonctionnalités à coté pendant que la release se constitue (ils ne sont pas bloqués)
* **hotfix** : branche utilisée pour corriger des bugs du livrable lorsqu’il est en production (master)
* **bugfix** : branche servant à fixer les bugs (pas utilisé)
* **support** : inutilisée


## Commandes git flow
Avant de commencer vous devez vous situer dans la branche **develop**.
Pour vous y positionner, utilisez la commande : 
`git checkout develop`

Maintenant, je peux commencer à coder...

Note : *Quand un item est clos (feature, release, hotfix) alors la branche est supprimée (définitivement dans le cas du hotfix)*

### Feature
Je créé une feature SI j'ai une fonctionnalité à développer.
Si ma feature existe déjà et n'est pas fermée, je me repositionne dessus si je n'y suis plus :
`git checkout feature/nom`

Pour créer une feature : 
`git flow feature start nom`

Pour clore une feature : 
`git flow feature finish nom`

Lorsque la feature est fermée (finish), elle est merge sur develop et supprimée.
Je suis rebasculé sur la branche **develop**.

### Release
**Une unique personne** crééra les releases *en fin de sprint* et sera chargée de consulter les autres membres de l'équipe pour les possibles merges dans le code.
La release contiendra l'ensemble des features créées durant le sprint.

Pour créer une release : 
`git flow release start nom_version`

Pour clore une release : 
`git flow release finish nom_version`

*Une fois qu’on met fin à la release, si on ne l’a pas indiqué, un tag sera demandé pour décrire le merge de la release et également un message pour indiquer l’importance du merge.*

Lorsque la release est fermée (finish), elle est merge sur develop et master et supprimée.
Je suis rebasculé sur la branche **develop**.

### Hotfix
Je créé un hotfix s'il y a un bug **urgent** à régler sur une fonctionnalité déjà en production et nécessitée par le client dans l'immédiat. Cela a peu de chances de nous arriver.
Pour créer un hotfix : 
`git flow hotfix start nom`

Pour clore un hotfix : 
`git flow hotfix finish nom_version`

Lorsque la branche hotfix est fermée (finish), elle est mergée sur master et supprimée définitivement.
Je suis rebasculé sur la branche **develop**.

## Ajouter du contenu dans des branches 
Je peux ajouter du contenu dans une branche (hotfix, feature, release) quand :
* la branche à été créée avec un "start"
* L'ajout de ce contenu correspond à mes besoins git flow (je suis sur la bonne branche)
* la branche n'est pas "finish" (fermée)

Pour ajouter du contenu sur ma branche (sur laquelle je me serais positionné au préalable) et push sur le git : 
```
git status
git add mes_fichiers
git commit -m "MESSAGE EXCPLICITE"
git push
```
## D'autres commandes
Observer l'arbre git : 
`gitk`

## Liens utiles
Voici un ensemble de liens pour mieux cerner le principe git flow :
[https://blog.engineering.publicissapient.fr/2018/03/28/gitflow-est-il-le-workflow-dont-jai-besoin/](https://blog.engineering.publicissapient.fr/2018/03/28/gitflow-est-il-le-workflow-dont-jai-besoin/)
[https://blog.nathanaelcherrier.com/fr/gitflow-la-methodologie-et-la-pratique/](https://blog.nathanaelcherrier.com/fr/gitflow-la-methodologie-et-la-pratique/)
[https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
