# Chess Tournament

 L'objectif de ce projet est de mettre en place un programme permettant d'organiser des tournois d'échecs et de conserver les données qui y sont liées.



## Table of Contents
- [Chess Tournament](#chess-tournament)
  - [Table of Contents](#table-of-contents)
  - [General Information](#general-information)
  - [Technologies Used](#technologies-used)
  - [Features](#features)
  - [Setup](#setup)
  - [Usage](#usage)
  - [Project Status](#project-status)

## General Information

 Ce programme permet de maintenir une base de donnée contenant les informations des différents joueurs.
 Un tournois peut être créer par l'utilisateur avec les joueurs présents dans la base de données.
 Une fois un tournois crée,le programme permet a l'utilisateur de générer une liste des matchs opposants les joueurs pour un tour selon le système suisse des tournois.
 L'utilisateur doit ensuite déclarer le début puis la fin du round, moment durant lequel il rentre le resultat des matchs,avant de pouvoir accéder au round suivant.
 Une fois un tournois fini il est automatiquement sauvegardé et l'utilisateur peut y accéder grâce a l'option générer un rapport dans le menu intéragir
 avec les données.
 De même il peut modifier le classement des joueurs en fonction de leurs résultats depuis ce même menu.

 Le programme contient une base de données remplie de joueurs et tournois fictifs pour les besoin d'une éventuelle démonstration.Vous pouvez remettre la base de donnée a zero en supprimant le fichier database.json dans le dossier data.

## Technologies Used
 - Tech 1 - TinyDb
 - Tech 2 - Time
 - Tech 3 - Datetime

## Features
 Liste des features
 - Ajouter un Joueur a la base de donnée.
 - Créer un Tournois.
 - Générer les matchs d'un tournois selon le système suisse.
 - Sauvegarder et charger un tournois a n'importe quelle étape.
 - Génerer des rapports sur les joueurs dans la base de données.
 - Générer des rapports sur les tournois dans la base de données.
 - Mettre a jour les classements des joueurs.

## Setup
 Pour faire fonctionner ce script,vous aurez besoin d'une version de Python3.8 ou supérieure et des packages décrits dans le fichier requirements.txt.Vous pouvez les installer dans un environement virtuel séparé en suivant ces étapes*:
 - Dans votre terminal,naviguez jusqu'au dossier où le script est présent.
 - Créez un nouvel environement virtuel en utilisant 'python -m venv env'
 - Activez votre environement virtuel avec 'env/scripts/activate'
 - Installez les packages nécessaire avec 'pip install -r requirements.txt'

 (Les étapes peuvent être différentes sur un OS différent de windows)

## Usage

 Après vous êtres assuré que les packages nécessaire sont installés,vous pouvez lancer le script en tappant 'main.py" dans votre terminal.

 Le programme affichera le menu principal,ce dernier,comme tout les menus du programmes sont navigables en rentrant un chiffre correspondant a l'option désirée dans le menu.Il vous sera parfois demandé de confirmé une action par les lettres Y pour oui ou N pour non.

 Vous pourrez ajouter des joueurs a la base de donnée a partir du menu intéragir avec les données.Il vous faudra au moins 8 joueurs présent dans la base de données pour pouvoir créer un tournois.
 A partir du menu principal l'utilisateur peut choisir l'option créer un tournois,ce qui lui demandera de fournir les informations nécessaires a la création du tournois.Après confirmation ce dernier sera sauvegardé dans la base de donnée des tournois en cours.

 Quand un tournois est présent dans la base de donnée des tournois en cours,l'utilisateur peut choisir la première option du menu principal pour charger le tournois désiré,a partir de là il aura accès au menu du tournois en cours.

 Ce dernier permet d'afficher divers information sur le tournois ainsi que d'accéder au round en cours.Depuis le menu du round,l'utilisateur doit d'abord choisir l'option préparer les pairs pour le round de manière a créer la liste des matchs.Il peut accéder a cette dernière a tout moment depuis le menu du round.
 Une fois les pairs générés l'utilisateur peut lancer le round a sa discrétion,ce qui démarera le chronomètre.
 Enfin une fois le round fini l'utilisateur doit marquer le round comme fini avant d'enregistrer le résultat des matchs.
 Une fois un round fini et les résultats rentrés l'utilisateur est automatiquement redirigé vers le menu du round suivant.

 L'utilisateur a aussi plusieurs possibilités offerte par par le menu "Intéragir avec les données";il peut entre autre:
 -Modifier rapidement le classement des joueurs
 -Modifier diverses données en cas d'érreur de saisie
 -Générer divers rapports sur les joueurs ou les tournois sauvegardés.

 Vous pouvez a tout moment générer un nouveau rapport Flake8 grâce a la commande:
 """
  flake8 "Path_to_file" --max-line-length=119 --exclude=env/ --format=html --htmldir=flake8_rapport 
  """


## Project Status

 Project is: _completed_