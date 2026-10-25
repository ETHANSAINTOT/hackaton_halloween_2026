# PUMPKIN SCREAM

**Pumpkin Scream** est un jeu d'arcade sur le thème d'Halloween, réalisé en Python avec Pygame pendant le hackathon Halloween 2026 d'Epitech (B-INN-000).

Vous incarnez un screamer qui se déplace de gauche à droite pour attraper les citrouilles qui tombent du ciel… tout en évitant les citrouilles maléfiques et les fantômes !

## Sommaire

- [Le jeu](#le-jeu)
- [Fonctionnalités](#fonctionnalités)
- [Structure du projet](#structure-du-projet)
- [1. Prérequis](#1-prérequis)
- [2. Téléchargement du projet](#2-téléchargement-du-projet)
- [3. Lancement du projet](#3-lancement-du-projet)
- [4. En savoir plus sur les mécaniques du jeu](#4-en-savoir-plus-sur-les-mécaniques-du-jeu-et-leur-apparition)

## Le jeu

Des objets tombent à la verticale depuis le haut de l'écran, à des positions et des vitesses aléatoires :

| Objet | Effet |
|---|---|
| Citrouille classique | +1 point |
| Citrouille sculptée | −1 vie |
| Fantôme | Mort immédiate |
| Bonbon (rare) | +3 points |
| Potion (rare) | Invincible pendant 3 secondes |

Vous commencez avec **5 vies** et la partie s'arrête quand vous n'en avez plus.
Tous les 10 points, vous passez au niveau suivant : les objets tombent plus souvent et plus vite, et à partir du niveau 3, les fantômes se mettent à onduler.
Si votre score fait partie des **5 meilleurs** jamais réalisés, vous pouvez entrer votre pseudo pour apparaître dans le leaderboard.

### Commandes

| Touche | Action |
|---|---|
| ← / → | Se déplacer |
| P | Mettre en pause / reprendre |
| Échap | Revenir au menu principal (la partie est perdue) |
| Entrée | Enregistrer son pseudo en fin de partie |

## Fonctionnalités

- **Menu principal** : boutons PLAY, RULES, LEADERBOARD et QUIT, avec effets au survol et au clic.
- **Écran des règles** du jeu.
- **Leaderboard** du top 5, avec l'or, l'argent et le bronze pour le podium.
- **Difficulté progressive** sur 10 niveaux.
- **Bonus** : bonbon et potion d'invincibilité.
- **Pause** et abandon de la partie à tout moment.
- **Écran de fin** avec saisie du pseudo et sauvegarde du score.
- **Son** : musiques d'ambiance (une pour les menus, une pour la partie) et effets sonores.

## Structure du projet

```
hackaton_halloween_2026/
├── assets/                    # Images, polices, musiques et sons
│   ├── buttons/               # Boutons des menus
│   ├── font/                  # bloody_ghost.otf (titres) et ARIAL.TTF (textes)
│   └── music/                 # Musiques d'ambiance et effets sonores
├── docs/
│   └── game.md                # Mécaniques du jeu en détail
└── src/
    ├── main.py                # Point d'entrée et menu principal
    ├── game_window.py         # La partie et l'écran de fin
    ├── rules.py               # Écran des règles
    ├── leaderboard_window.py  # Écran du leaderboard et sauvegarde des scores
    ├── ui.py                  # Composants partagés (boutons, panneaux, musique)
    ├── constants.py           # Tous les réglages du jeu
    └── leaderboard.csv        # Top 5 des scores
```

## 1. Prérequis

* Python : https://www.python.org/downloads/
* Git : https://git-scm.com/install/
* Pygame (nécessite Python avec pip)

```bash
pip install pygame
```

ou

```bash
pip install pygame-ce
```

> Si `pip` refuse l'installation avec l'erreur `externally-managed-environment` (courant sur Linux), installez Pygame dans un environnement virtuel, depuis le dossier du projet :
>
> ```bash
> python3 -m venv .venv
> ```
>
> ```bash
> source .venv/bin/activate
> ```
>
> ```bash
> pip install pygame
> ```
>
> Pensez ensuite à réactiver l'environnement (`source .venv/bin/activate`) avant chaque lancement du jeu.

## 2. Téléchargement du projet

Exécutez cette commande :

```bash
git clone git@github.com:ETHANSAINTOT/hackaton_halloween_2026.git
```

ou, si vous n'avez pas de clé SSH configurée sur GitHub :

```bash
git clone https://github.com/ETHANSAINTOT/hackaton_halloween_2026.git
```

## 3. Lancement du projet

Rendez-vous dans le dossier du projet :

```bash
cd hackaton_halloween_2026
```

puis lancez le jeu avec :

```bash
python src/main.py
```

> Sur Linux et macOS, la commande est souvent `python3` au lieu de `python`.

## 4. En savoir plus sur les mécaniques du jeu et leur apparition

Tout le détail du fonctionnement du jeu est dans la documentation des mécaniques : **[docs/game.md](docs/game.md)**.

Vous y trouverez :

- l'effet de chaque objet et le fonctionnement des collisions ;
- les probabilités d'apparition de chaque objet (« une chance sur combien ») ;
- le tableau des 10 niveaux de difficulté (délais, vitesses, ondulation des fantômes) ;
- le fonctionnement de la pause, de la fin de partie et du leaderboard ;
- la liste des réglages modifiables dans `src/constants.py`.
