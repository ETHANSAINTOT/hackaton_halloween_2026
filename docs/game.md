# Pumpkin Scream : mécaniques du jeu

[← Retour à la documentation principale (README)](../README.md)

Ce document explique en détail comment fonctionne une partie : les objets, les vies, les niveaux, le hasard, le leaderboard et les sons.
Toutes les valeurs citées se règlent dans [`src/constants.py`](../src/constants.py) et la logique de jeu se trouve dans [`src/game_window.py`](../src/game_window.py).

## Sommaire

1. [Déroulement d'une partie](#1-déroulement-dune-partie)
2. [Commandes](#2-commandes)
3. [Les objets](#3-les-objets)
4. [Score, vies et niveaux](#4-score-vies-et-niveaux)
5. [Les fantômes qui ondulent](#5-les-fantômes-qui-ondulent)
6. [Le hasard](#6-le-hasard)
7. [Pause, abandon et fin de partie](#7-pause-abandon-et-fin-de-partie)
8. [Le leaderboard](#8-le-leaderboard)
9. [Musiques et sons](#9-musiques-et-sons)
10. [Modifier les réglages](#10-modifier-les-réglages)

## 1. Déroulement d'une partie

1. Depuis le menu principal, le bouton **PLAY** lance une partie.
2. Le screamer apparaît au centre de l'écran, posé sur le sol, avec **5 vies** et **0 point**.
3. Des objets tombent du haut de l'écran : il faut attraper les bons et éviter les mauvais.
4. Plus le score monte, plus le **niveau** augmente : les objets tombent plus souvent et plus vite.
5. La partie s'arrête quand il ne reste plus aucune vie. Un écran de fin affiche le score et, si celui-ci entre dans le top 5, permet d'enregistrer un pseudo.

Le nombre de vies, le score et le niveau sont affichés en permanence en haut à gauche de l'écran (`Health`, `Score`, `Level`).

## 2. Commandes

### Pendant la partie

| Touche / action | Effet |
|---|---|
| Flèche **gauche** / **droite** | Déplace le screamer (on peut garder la touche enfoncée) |
| **P** | Met le jeu en pause, ou le relance |
| **Échap** | Retour au menu principal (la partie est perdue) |
| Bouton **QUIT** (en haut à droite) | Pareil qu'Échap ; un avertissement s'affiche quand on le survole |

Le screamer se déplace à 600 pixels par seconde et ne peut pas sortir de l'écran. Il ne bouge qu'horizontalement.

### Sur l'écran de fin

| Touche / action | Effet |
|---|---|
| Clavier | Écrit le pseudo (16 caractères maximum), si le score entre dans le top 5 |
| **Retour arrière** | Efface le dernier caractère |
| **Entrée** | Enregistre le score dans le leaderboard et revient au menu |
| **Échap** | Revient au menu **sans** enregistrer |
| Bouton **PLAY** | Relance directement une nouvelle partie, **sans** enregistrer |

## 3. Les objets

| Objet | Image | Effet au contact | Son |
|---|---|---|---|
| Citrouille classique | `assets/pumpkin.png` | **+1 point** | `good.mp3` |
| Citrouille sculptée | `assets/pumpkin_carved.png` | **−1 vie** | `pain.mp3` (`scream.mp3` si c'était la dernière vie) |
| Fantôme | `assets/boo.png` | **Mort immédiate** (5 dégâts, soit toutes les vies) | `scream.mp3` |
| Bonbon | `assets/candy.png` | **+3 points** | `good.mp3` |
| Potion | `assets/potion.png` | **Invincibilité pendant 3 secondes** | `good.mp3` |

Quelques précisions :

- **Contact** : un objet est attrapé dès que son carré (64 × 64 pixels) touche le rectangle de l'image du screamer (120 × 180 pixels). Ce rectangle inclut les zones transparentes autour du personnage, donc frôler le screamer suffit.
- **Sol** : un objet qui atteint le sol (à 700 pixels du haut de l'écran) disparaît sans aucun effet. Rater une citrouille ne fait donc pas perdre de vie.
- **Invincibilité** : pendant l'effet de la potion, le screamer devient bleuté. Les citrouilles sculptées et les fantômes qu'il touche disparaissent sans lui faire de dégâts, tandis que les citrouilles et les bonbons rapportent toujours leurs points.
- **Potion sur potion** : prendre une potion pendant l'effet d'une autre remet le compteur à 3 secondes. Les durées ne s'additionnent pas.

## 4. Score, vies et niveaux

- **Vies** : la partie commence avec 5 vies (`SCREAMER_HEALTH`). Une citrouille sculptée en retire une, un fantôme les retire toutes.
- **Score** : +1 par citrouille, +3 par bonbon.
- **Niveau** : on monte d'un niveau tous les **10 points** (`SCORE_PER_LEVEL`), jusqu'au **niveau 10** maximum (`MAX_LEVEL`).

Chaque niveau rend le jeu plus difficile de deux façons :

- **Délai entre deux objets** : il est multiplié par `1 − 0,1 × (niveau − 1)`, sans jamais descendre sous `0,3` (`SPAWN_DELAY_STEP`).
- **Vitesse de chute** : les bornes minimale et maximale augmentent de **40 pixels par seconde** par niveau (`FALL_SPEED_STEP`).

| Niveau | Score | Délai entre deux objets | Objets par minute (en moyenne) | Vitesse de chute | Durée de la chute | Fantômes |
|---|---|---|---|---|---|---|
| 1 | 0 à 9 | 0,5 à 1,5 s | 60 | 150 à 400 px/s | 1,75 à 4,7 s | tout droit |
| 2 | 10 à 19 | 0,45 à 1,35 s | ≈ 67 | 190 à 440 px/s | 1,6 à 3,7 s | tout droit |
| 3 | 20 à 29 | 0,4 à 1,2 s | 75 | 230 à 480 px/s | 1,5 à 3 s | **ondulent** |
| 4 | 30 à 39 | 0,35 à 1,05 s | ≈ 86 | 270 à 520 px/s | 1,35 à 2,6 s | ondulent |
| 5 | 40 à 49 | 0,3 à 0,9 s | 100 | 310 à 560 px/s | 1,25 à 2,3 s | ondulent |
| 6 | 50 à 59 | 0,25 à 0,75 s | 120 | 350 à 600 px/s | 1,2 à 2 s | ondulent |
| 7 | 60 à 69 | 0,2 à 0,6 s | 150 | 390 à 640 px/s | 1,1 à 1,8 s | ondulent |
| 8 | 70 à 79 | 0,15 à 0,45 s | 200 | 430 à 680 px/s | 1 à 1,6 s | ondulent |
| 9 | 80 à 89 | 0,15 à 0,45 s | 200 | 470 à 720 px/s | 0,97 à 1,5 s | ondulent |
| 10 | 90 et plus | 0,15 à 0,45 s | 200 | 510 à 760 px/s | 0,92 à 1,4 s | ondulent |

À partir du niveau 8, les objets n'apparaissent plus plus souvent (le délai a atteint son minimum), mais ils continuent à tomber plus vite jusqu'au niveau 10.

La durée de la chute correspond aux 700 pixels qui séparent le haut de l'écran du sol.
La vitesse et le délai sont tirés au moment où l'objet apparaît, avec le niveau de ce moment-là : un objet déjà en train de tomber ne change pas de vitesse quand on monte de niveau.

## 5. Les fantômes qui ondulent

À partir du **niveau 3** (`SWAY_LEVEL`), les fantômes ne tombent plus tout droit : ils se balancent de gauche à droite en suivant une sinusoïde.

- **Amplitude** : 80 pixels de chaque côté de leur position de départ (`SWAY_AMPLITUDE`).
- **Rythme** : un aller-retour complet dure environ **3,1 secondes** (`SWAY_SPEED` vaut 2, et 2π ÷ 2 ≈ 3,14).
- **Départ** : le fantôme part toujours d'abord vers la droite.
- **Bords** : le mouvement est bloqué aux bords de l'écran, un fantôme ne sort jamais de la fenêtre.
- **Niveau pris en compte** : c'est le niveau au moment où le fantôme apparaît qui compte. Un fantôme apparu au niveau 2 continue de tomber tout droit, même si le joueur passe au niveau 3 pendant sa chute.

Les citrouilles, bonbons et potions tombent toujours à la verticale.

## 6. Le hasard

Tout le hasard du jeu passe par le module `random` de Python, sans graine fixe : deux parties ne sont jamais identiques.
Pour chaque objet qui tombe, quatre choses sont tirées au sort :

1. son **type** ;
2. le **moment** où il apparaît ;
3. sa **position** sur le bord haut de la fenêtre ;
4. sa **vitesse** de chute.

Le screamer, lui, n'a rien d'aléatoire : il démarre toujours au centre et ne bouge qu'avec les flèches.

### 6.1 Quel objet tombe ?

Le tirage se fait en deux étapes, à chaque nouvel objet :

1. **Les poids sont tirés au hasard.** Chaque objet a un intervalle de poids dans `FALLING_OBJECTS`, et un poids entier est tiré dans cet intervalle avec `random.randint`, toutes les valeurs ayant la même chance.
2. **L'objet est choisi selon ces poids** avec `random.choices` : plus le poids d'un objet est grand par rapport aux autres, plus il a de chances d'être choisi.

Comme les poids changent à chaque tirage, la probabilité finale n'est pas un simple « poids ÷ total ». Elle a été calculée exactement en faisant la moyenne sur les 96 combinaisons de poids possibles, puis vérifiée par une simulation d'un million de tirages :

| Objet | Intervalle de poids | Probabilité | Une chance sur… |
|---|---|---|---|
| Citrouille classique | 3 à 6 | ≈ 50,1 % | environ **1 sur 2** |
| Citrouille sculptée | 1 à 3 | ≈ 22,1 % | environ **1 sur 4,5** |
| Fantôme | 1 à 2 | ≈ 16,9 % | environ **1 sur 6** |
| Bonbon | 0 à 1 | ≈ 5,4 % | environ **1 sur 18,5** |
| Potion | 0 à 1 | ≈ 5,4 % | environ **1 sur 18,5** |

- **Bonbon et potion** : leur poids vaut 0 une fois sur deux. Dans ce cas, ils ne peuvent pas du tout sortir lors de ce tirage, ce qui les rend rares. Ils ont exactement la même probabilité l'un que l'autre.
- **Tirages indépendants** : le jeu ne « compense » pas d'un objet à l'autre. Par exemple, la chance que deux fantômes tombent à la suite est d'environ 16,9 % × 16,9 %, soit **1 chance sur 35**.

En moyenne, cela donne par minute :

| Objet | Niveau 1 (60 objets par minute) | Niveau 8 et plus (200 objets par minute) |
|---|---|---|
| Citrouilles classiques | ≈ 30 | ≈ 100 |
| Citrouilles sculptées | ≈ 13 | ≈ 44 |
| Fantômes | ≈ 10 | ≈ 34 |
| Bonbons | ≈ 3 | ≈ 11 |
| Potions | ≈ 3 | ≈ 11 |

Ce sont des moyennes : sur une vraie partie, les chiffres varient autour de ces valeurs.

### 6.2 Quand un objet apparaît-il ?

Après chaque apparition, le délai avant l'objet suivant est tiré avec `random.uniform` entre **0,5 et 1,5 seconde** (`SPAWN_DELAY_MIN`, `SPAWN_DELAY_MAX`). Toutes les durées de l'intervalle ont la même chance d'être choisies. Ce délai est ensuite raccourci selon le niveau (voir le [tableau des niveaux](#4-score-vies-et-niveaux)).

Au niveau 1, le délai moyen est de **1 seconde**, soit environ 60 objets par minute.

### 6.3 Où l'objet apparaît-il ?

La position horizontale est tirée avec `random.randint` entre **0 et 1216 pixels**. 1216 correspond à la largeur de la fenêtre (1280) moins la taille d'un objet (64), pour qu'il ne dépasse jamais du bord droit.

- **Probabilité** : il y a 1217 positions possibles, chacune avec **1 chance sur 1217**. Aucun côté de l'écran n'est favorisé.
- **Apparition** : l'objet apparaît juste au-dessus du bord haut de la fenêtre, puis tombe à la verticale. Seuls les fantômes à partir du niveau 3 se décalent (voir la [section 5](#5-les-fantômes-qui-ondulent)).
- **Chevauchement** : rien n'empêche deux objets de tomber au même endroit ou de se chevaucher.

### 6.4 À quelle vitesse tombe-t-il ?

La vitesse est tirée avec `random.uniform` entre **150 et 400 pixels par seconde** au niveau 1 (`FALL_SPEED_MIN`, `FALL_SPEED_MAX`), avec 40 pixels par seconde de plus par niveau (voir le [tableau des niveaux](#4-score-vies-et-niveaux)).

- **Constante** : la vitesse est choisie une seule fois, quand l'objet apparaît, puis reste la même pendant toute la chute.
- **Même règle pour tous** : elle ne dépend pas du type d'objet. Un fantôme peut tomber aussi vite ou aussi lentement qu'une citrouille.

## 7. Pause, abandon et fin de partie

### Pause

La touche **P** fige complètement la partie : le screamer ne bouge plus, les objets s'arrêtent et plus rien n'apparaît. Un voile sombre s'affiche avec « Paused » et « Press P to resume ». Pendant la pause, Échap et le bouton QUIT fonctionnent toujours.

### Abandon

**Échap** ou le bouton **QUIT** ramènent immédiatement au menu principal. La partie en cours est perdue et le score n'est pas enregistré. Au survol du bouton QUIT, une bulle le rappelle : *« You will go back to the main menu and lose all your progress! »*

### Fin de partie

Quand la dernière vie est perdue, le jeu joue un cri (`scream.mp3`) et affiche l'écran de fin. On y trouve une image plein écran (`true_screamer.png`) et le score final en haut.

Si le score entre dans le top 5, le message *« You made the top 5 ! Enter your nickname : »* apparaît avec une zone de saisie. Voir les [commandes de l'écran de fin](#sur-lécran-de-fin) pour enregistrer, revenir au menu ou rejouer.

Points d'attention :

- **Enregistrement** : le score n'est enregistré qu'en appuyant sur **Entrée** avec un pseudo non vide. Échap, le bouton PLAY ou un pseudo vide ne l'enregistrent pas.
- **Rejouer** : le bouton PLAY lance une nouvelle partie remise à zéro (5 vies, 0 point, niveau 1).

## 8. Le leaderboard

Les 5 meilleurs scores sont stockés dans `src/leaderboard.csv`, avec un point-virgule comme séparateur :

```csv
nickname;score
player1;42
player2;30
```

- **Ordre** : le fichier est trié du meilleur score au moins bon. L'écran Leaderboard du menu l'affiche dans cet ordre : 1er en or, 2e en argent, 3e en bronze.
- **Conditions pour entrer dans le top 5** : le fichier contient moins de 5 scores, ou le score est **strictement supérieur** au 5e. Égaler le 5e ne suffit pas.
- **Sauvegarde** : le nouveau score est ajouté, la liste est triée de nouveau, puis seuls les 5 meilleurs sont gardés dans le fichier.
- **Interdiction** : comme le rappellent les règles du jeu, toute modification manuelle de `leaderboard.csv` est strictement interdite. Seul un score du top 5 peut y entrer.

## 9. Musiques et sons

| Fichier (`assets/music/`) | Quand ? |
|---|---|
| `spooky_halloween.mp3` | En boucle dans le menu principal, les règles et le leaderboard |
| `spooky_scary_skeleton.mp3` | En boucle pendant la partie (et sur l'écran de fin) |
| `good.mp3` | Citrouille, bonbon ou potion attrapés |
| `pain.mp3` | Vie perdue à cause d'une citrouille sculptée |
| `scream.mp3` | Dernière vie perdue |

Le volume de la musique et des sons est réglé à 50 % (`MUSIC_VOLUME`). Si l'ordinateur n'a pas de sortie audio, le jeu fonctionne quand même, sans son.

## 10. Modifier les réglages

Tout se change dans [`src/constants.py`](../src/constants.py) :

| Constante | Rôle | Valeur actuelle |
|---|---|---|
| `SCREAMER_HEALTH` | Nombre de vies au départ | 5 |
| `SCREAMER_SPEED` | Vitesse du screamer (pixels par seconde) | 600 |
| `FALLING_OBJECTS` | Objets, intervalles de poids, dégâts et points | voir la [section 6.1](#61-quel-objet-tombe-) |
| `POTION_DURATION` | Durée de l'invincibilité (secondes) | 3 |
| `SPAWN_DELAY_MIN` / `SPAWN_DELAY_MAX` | Délai entre deux objets au niveau 1 (secondes) | 0,5 / 1,5 |
| `FALL_SPEED_MIN` / `FALL_SPEED_MAX` | Vitesse de chute au niveau 1 (pixels par seconde) | 150 / 400 |
| `SCORE_PER_LEVEL` | Points nécessaires pour monter d'un niveau | 10 |
| `MAX_LEVEL` | Niveau maximum | 10 |
| `SPAWN_DELAY_STEP` | Réduction du délai par niveau | 0,1 (10 %) |
| `FALL_SPEED_STEP` | Vitesse de chute ajoutée par niveau (pixels par seconde) | 40 |
| `SWAY_LEVEL` | Niveau à partir duquel les fantômes ondulent | 3 |
| `SWAY_AMPLITUDE` / `SWAY_SPEED` | Amplitude (pixels) et rythme de l'ondulation | 80 / 2 |
| `OBJECT_SIZE` | Taille d'un objet (pixels) | 64 |
| `MUSIC_VOLUME` | Volume de la musique et des sons (0.0 à 1.0) | 0.5 |

Par exemple, pour rendre les fantômes plus rares, il suffit de réduire leur intervalle de poids dans `FALLING_OBJECTS`, en passant de `(1, 2)` à `(0, 1)`. Attention : changer un intervalle modifie aussi la probabilité de tous les autres objets, et les pourcentages de la [section 6.1](#61-quel-objet-tombe-) doivent alors être recalculés.

---

[← Retour à la documentation principale (README)](../README.md)
