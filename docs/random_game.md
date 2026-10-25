# L'aléatoire dans Pumpkin Scream

Tout le hasard du jeu passe par le module `random` de Python, sans graine fixe : deux parties ne seront jamais identiques.
Le code se trouve dans `src/game_window.py` et toutes les valeurs se règlent dans `src/constants.py`.

Quatre choses sont tirées au sort pour chaque objet qui tombe :

1. le **type** d'objet ;
2. le **moment** où il apparaît ;
3. sa **position** sur le bord haut de la fenêtre ;
4. sa **vitesse** de chute.

Le personnage (le screamer), lui, n'a rien d'aléatoire : il démarre au centre et ne bouge qu'avec les flèches.

## 1. Quel objet tombe ?

Le type est tiré avec `random.choices`, en utilisant un **poids** par objet (`FALLING_OBJECTS`).
La probabilité d'un objet est son poids divisé par la somme des poids (ici 6 + 3 + 1 = 10).

| Objet | Image | Poids | Probabilité | Une chance sur… |
|---|---|---|---|---|
| Citrouille classique | `pumpkin.png` | 6 | 60 % | 3 chances sur 5 (environ 1 sur 1,7) |
| Citrouille sculptée | `pumpkin_carved.png` | 3 | 30 % | 3 chances sur 10 (environ 1 sur 3,3) |
| Fantôme | `boo.png` | 1 | 10 % | **1 chance sur 10** |

Chaque tirage est indépendant des précédents : le jeu ne « compense » pas.
Par exemple, la chance que deux fantômes tombent à la suite est de 1 sur 10 × 1 sur 10, soit **1 chance sur 100**.

## 2. Quand un objet apparaît-il ?

Après chaque apparition, le délai avant l'objet suivant est tiré avec `random.uniform` entre **0,5 et 1,5 seconde** (`SPAWN_DELAY_MIN`, `SPAWN_DELAY_MAX`).
Toutes les durées de cet intervalle ont la même chance d'être choisies, donc le délai moyen est de **1 seconde**.

En moyenne, sur une minute, il tombe donc environ :

| Objet | Par minute (en moyenne) |
|---|---|
| Tous les objets | 60 |
| Citrouilles classiques | 36 |
| Citrouilles sculptées | 18 |
| Fantômes | 6 (un toutes les 10 secondes) |

Ce sont des moyennes : sur une partie réelle, les chiffres varient autour de ces valeurs.

## 3. Où l'objet apparaît-il ?

La position horizontale est tirée avec `random.randint` entre **0 et 1216 pixels**.
1216 correspond à la largeur de la fenêtre (1280) moins la taille d'un objet (64), pour qu'il ne dépasse jamais du bord droit.

- Il y a 1217 positions possibles, chacune avec **1 chance sur 1217**.
- Toute la largeur de la fenêtre est couverte de la même façon : aucun côté n'est favorisé.
- L'objet apparaît juste au-dessus du bord haut de la fenêtre, puis tombe **à la verticale** : sa position horizontale ne change plus.
- Rien n'empêche deux objets de tomber au même endroit ou de se chevaucher.

## 4. À quelle vitesse tombe-t-il ?

La vitesse est tirée avec `random.uniform` entre **150 et 400 pixels par seconde** (`FALL_SPEED_MIN`, `FALL_SPEED_MAX`).
Elle est choisie une seule fois, à l'apparition, puis reste la même pendant toute la chute.

L'objet parcourt 700 pixels avant de toucher le sol (`GROUND_Y`), où il disparaît. Sa chute dure donc :

- au plus vite : 700 ÷ 400 = **1,75 seconde** ;
- au plus lent : 700 ÷ 150 ≈ **4,7 secondes**.

La vitesse ne dépend pas du type d'objet : un fantôme peut tomber aussi vite ou aussi lentement qu'une citrouille.

## Modifier les réglages

Tout se change dans `src/constants.py` :

| Constante | Rôle | Valeur actuelle |
|---|---|---|
| `FALLING_OBJECTS` | Objets possibles et leur poids | 6 / 3 / 1 |
| `SPAWN_DELAY_MIN` / `SPAWN_DELAY_MAX` | Délai entre deux objets (secondes) | 0,5 / 1,5 |
| `FALL_SPEED_MIN` / `FALL_SPEED_MAX` | Vitesse de chute (pixels par seconde) | 150 / 400 |
| `OBJECT_SIZE` | Taille d'un objet (pixels) | 64 |

Par exemple, pour rendre les fantômes deux fois plus fréquents, il suffit de passer leur poids de 1 à 2 : ils auront alors 2 chances sur 11.
