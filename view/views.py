"""Base view"""

import time
from datetime import timedelta


class Views():
    """Implement other views"""

    # Input for navigation #

    def ask_for_input(self):
        """ask the user to select an option and return it"""
        choice = input("Veuillez entrer votre choix:\n")
        return choice

    def incorrect_input(self):
        """print for incorrect input"""
        print(
            "Vous devez rentrer un chiffre correspondant a l'option voulu\n"
            "S'il vous plaît reessayez\n"
            )

    def confirmation(self):
        """Ask user for a confirmation before sensitive actions"""
        prompt = "Tapez 'Y' pour poursuivre,'N' pour abandonner\n"
        choice = input(prompt).lower()
        if choice == 'y':
            return choice
        elif choice == "n":
            return choice
        else:
            print("Veuillez répondre par Y pour oui ou N pour non\n")
            self.confirmation()

    # Main menu display #

    def main_menu_display(self):
        """Display the main menu"""
        print(
            "\n--Menu Principal--\n"
            "\n1.Charger un tournois en cours"
            "\n2.Créer un Tournois"
            "\n3.Intéragir avec les données"
            "\n4.Sortir du programme\n"
        )

    def data_menu_display(self):
        """display menu to interact with data"""
        print(
            "\n --Base de donnée--"
            "\n1.Ajouter un joueur"
            "\n2.Génerer un rapport"
            "\n3.Retour au menu\n"
        )

    def display_ongoing_tournament_list(self, ongoing_tournament_db):
        """print a list of saved tournament for the user to choose from"""
        print("Liste des tournois en cours:\n")
        for document in range(len(ongoing_tournament_db)):
            tournament_name = "Nom du tournois: " + ongoing_tournament_db[document]["tournament_name"]
            display = (
                "n°" + str(document+1) + ": " + tournament_name +
                f"; Index du tournois: {ongoing_tournament_db[document].doc_id}"
            )
            print(display)

    def no_tournament_at_index(self,tournament_index):
        print(f"Aucun tournois n'a l'index n°:{tournament_index}\n"
            "Veuillez rentrer une nouvelle valeur\n")

    def no_ongoing_tournament(self):
        """Print a message if no ongoing tournament in database"""
        print("Il n'y a pas de tournois en cours.\n")

    def goodbye(self):
        """Print an exist message"""
        print("Vous quittez le programme,au revoir")

    # Input to load tournament #

    def ask_for_tournament_to_load(self):
        """Ask for the index of the tournament to load"""
        prompt = "Veuillez rentrer le chiffre correspondant au tournois que vous souhaitez \n"
        tournament = input(prompt)
        return tournament

    # input for tournament creation #

    def ask_for_tournament_name(self):
        """input for tournament name"""
        prompt = ("Veuillez rentrer le nom du tournois\n")
        name = input(prompt)
        return name

    def ask_for_place(self):
        """input for tournament place"""
        prompt = ("Veuillez rentrer l'endroit où le tournois a lieu\n")
        place = input(prompt)
        return place

    def ask_for_date(self):
        """input for tournament date"""
        prompt = ("Veuillez indiquer la date de début du Tournois\n"
                "La date doit être au format jj/mm/aa\n")
        date = input(prompt)
        return date

    def incorrect_date_format(self):
        print("Vous la date que vous avez rentré n'est pas correcte;\n"
            "Elle doit être au format jj/mm/aa")

    def ask_time_controller(self):
        """input for time controller setting """
        prompt = (
            "Selectionnez la méthode de controlle du temps\n"
            "1.Bullet\n"
            "2.Blitz\n"
            "3.Coup rapide\n"
        )
        time = input(prompt)
        return time

    def ask_for_description(self):
        """input for tournament description"""
        prompt = "Veuillez ajouter une description du tournois\n"
        description = input(prompt)
        return description

    def select_player(self):
        """input for player selection"""
        prompt = "Veuillez rentrer le chiffre correspondant a l'index d'un joueur\n"
        player = input(prompt)
        return player

    def already_selected_player_error(self):
        print("Le joueur est déjà présent dans la liste,veuillez ajouter un autre joueur \n")


    def incorrect_player_index(self, player_index):
        """display index selection error"""
        print(
            f"Aucun joueur n'a l'index n°:{player_index}\n"
            "Veuillez rentrer une nouvelle valeur\n"
            )

    def display_selected_players(self,players):
        print("Index des joueurs déjà selectionés:\n")
        print(players)

    def player_selection_list_full(self,loaded_players):
        print("Liste des joueurs complète!\n"
        "Voici les joueurs selectionés:\n")
        for player in loaded_players:
            print(str(player)) #Substract one to match db as list starting from 0
        print("souhaitez vous créer un tournois avec ces joueurs?\n")

    def tournament_creation_confirmation(self, tournament):
        print("Souhaitez vous créer un tournois avec les paramètres suivants?")
        for key in tournament:
            print( str(key) + " :" + str(tournament[key]) + "\n")

    def tournament_creation_display(self,tournament_index):
        print("Création du tournois")
        print(f"Sauvegardé en tant que tournois n°{tournament_index}\n"
                "Chargez le tournois pour intéragir avec\n")

    def selected_players_display(self,playerlist):
        print("Les joueurs selectionnés sont:\n")
        print(playerlist + "\n")

    def return_to_menu_confirmation(self):
        print("Vous allez retourner au menu principal\n"
        "Veuillez confirmer?`n")

    # Tournament display #

    def tournament_menu_display(self):
        """Display the tournament menu"""
        prompt = (
            "--Menu du Tournois--\n"
            "1.Afficher la liste des joueurs\n"
            "2.Afficher le status des rounds\n"
            "3.Menu du round en cours\n"
            "4.Sauvegarder et retourner au menu principal\n"
        )
        print(prompt)

    def round_menu_display(self, round_index):
        """Display the menu for a round"""
        prompt = (
            f"--Menu du round {round_index + 1 }\n"
            "1.Afficher les pairs du round\n"
            "2.Préparer les pairs pour le round\n"
            "3.Démarer le round\n"
            "4.Marquer le round comme fini\n"
            "5.Retourner au menu du tournois \n"
            "6.Sauvegarder et retourner au menu principal \n"
        )
        print(prompt)

    def display_player_list(self,playerlist_sorted):
        liste = "Liste des joueurs par index du tournois: \n"
        for player in playerlist_sorted:
            liste += "\n" + str(player) + "\n"
        print(liste)

    def display_round_match_list(self, round):
        """print the list of matchs in a round"""
        for match in range(len(round.match_list)):
            print(round.match_list[match])

    def tournament_status(self, list_of_rounds):
        """print status of all rounds and the matchs they includes"""
        for round_number in range(len(list_of_rounds)):
            if list_of_rounds[round_number].status == "Ungenerated":
                print(f"Round n°{round_number+1}")
                print(f"Les pairs du round n°{round_number+1} n'ont pas été générée\n")
                break
            elif list_of_rounds[round_number].status == "Generated":
                print(f"Round n°{round_number+1}")
                print(
                    f"Les pairs du round n°{round_number} ont été générée mais le round n'a pas commencé\n"
                    "Voici la liste des matchs:\n"
                )
                self.display_round_match_list(list_of_rounds[round_number])
            elif list_of_rounds[round_number].status == "Started":
                print(f"Round n°{round_number+1}")
                self.round_chronometer_display(list_of_rounds[round_number])
                print("Voici la liste des matchs:\n")
                self.display_round_match_list(list_of_rounds[round_number])
            elif list_of_rounds[round_number].status == "Finished":
                print(f"Round n°{round_number+1}")
                self.round_chronometer_display(list_of_rounds[round_number])
                print("Voici la liste des matchs:\n")
                self.display_round_match_list(list_of_rounds[round_number])

    def round_chronometer_display(self, round):
        """Display a round chronometer"""
        if round.status == "Unplayed":
            print("Le round n'a pas débuté\n")
        elif round.status == "Started":
            current_time = time.time()
            elapsed_time_min = (timedelta(seconds=current_time - round.start_time))
            print(f"Le round a débuté il y a {elapsed_time_min} secondes\n")
        elif round.status == "Finished":
            elapsed_time_min = (timedelta(seconds=round.end_time - round.start_time))
            print(f"Le round est fini et a duré {elapsed_time_min} secondes\n")

    def start_round_confirmation(self):
        """ask for confirmation before starting round timer"""
        print(
            "Vous allez lancer le round,souhaitez vous confirmer? \n"
            "Le chronomètre du round sera lancé si vous confirmez\n"
            "pressez Y pour Oui,N pour non\n"
        )

    def end_round_confirmation(self):
        """ask for confirmation before ending round"""
        print(
            "Vous allez terminer le round,souhaitez vous confirmer? \n"
            "Le chronomètre du round sera arreté et vous devrez rentrer les resultats des matchs si vous confirmez\n"
            "pressez Y pour Oui,N pour non\n"
        )

    def error_match_list_not_generated(self):
        print("Les pairs n'ont pas encore été générée,"
                        " Veuillez choisir l'option 2")

    def error_match_list_already_generated(self):
        print("Les pair de joueurs ont déjà été généré,"
            "Vous pouvez démarrer le round en préssant l'option 3 dans le menu du round")

    def error_start_no_match_list(self):
        """error message for trying to start a round which match list is not generated yet"""
        print("Vous ne pouvez pas démarrer ce round parce que les matchs n'ont pas encore été générés\n")

    def error_start_already_started(self):
        """error message for trying to start a round already started"""
        print("Vous ne pouvez pas démarrer ce round parce qu'il a déjà débuté\n")

    def error_start_already_finished(self):
        """error message for trying to start a round alredy finished"""
        print("Vous ne pouvez pas démarrer ce round parce qu'il est déjà fini\n")

    def error_end_not_generated(self):
        """error message for trying to end a round which match list is not generated yet"""
        print("Vous ne pouvez pas finir ce round parce que les matchs n'ont pas encore été générés")

    def error_end_not_started(self):
        """error message for trying to end a round which is not started yet"""
        print("Vous ne pouvez pas finir ce round parce qu'il n'a pas débuté\n")

    def error_end_already_ended(self):
        """error message for trying to end a round which is already finished"""
        print("Vous ne pouvez pas finir ce round parce qu'il est déjà fini\n")

    def tournament_is_over(self, tournament_index):
        """Display message when the tournament is finished,with the index
        at which it was saved in the finished tournament db"""
        print(
                "Le tournois est terminé,il a été sauvegardé a l'index"
                f"{tournament_index} dans la base de donnée des tournois fini."
            )

    # Tournament related input #

    def player_list_display_choice(self):
        """ask for the method to display tournament playerlist"""
        prompt = (
            "Veuillez choisir la méthode de tri de la liste des joueurs:\n"
            "1.Afficher par index du tournois\n"
            "2.Afficher par score du tournois\n"
        )
        result = input(prompt)
        return result

    def match_result_prompt(self, match):
        """ask input for match result"""
        prompt = (
            "Rentrez le chiffre suivant en fonction du resultat:\n"
            f"1-Victoire du premier joueur: {match.first_player.give_full_name()}\n"
            f"2-Victoire du second joueur: {match.second_player.give_full_name()}\n"
            f"3-Match nul\n"
        )
        result = input(prompt)
        return result

    # Related to data display #


    def print_player_index_and_name(self, name, index):
        """display players name and index +1 to compensate for conversion of db into list """
        index = f"index du joueur: {index + 1},nom :" + name + "\n"
        print(index)

    # New player creation #

    def ask_for_family_name(self):
        """ask for a player family name"""
        prompt = ("Veuillez rentrer le nom de famille du joueur?\n")
        family_name = input(prompt)
        return family_name

    def ask_for_first_name(self):
        """ask for a player family name"""
        prompt = ("Veuillez rentrer le prénom du joueur?\n")
        first_name = input(prompt)
        return first_name


    def ask_for_gender(self):
        prompt = ("Veuillez rentrer M pour un homme ou F pour une femme\n")
        gender = input(prompt)
        if gender.lower() not in ["m","f"]:
            return self.ask_for_gender()
        else:
            return gender

    def ask_for_rank(self):
        prompt = ("Veuillez rentrer le rang du joueur\n")
        rank = input(prompt)
        return rank

    def player_created(self, player_dict, player_index):
        first_name = player_dict["first_name"]
        family_name = player_dict["family_name"]
        print(f"Le joueur {first_name} {family_name} a été sauvegardé a l'index {player_index} \n")