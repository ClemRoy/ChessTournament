#coding:utf-8

from os import system
import sys
from pathlib import Path
from tinydb import TinyDB
from tinydb.queries import Query
from tinydb.table import Document
from model.player import Player
from model.playerlist import Playerlist
from model.match import Match
from model.round import Round
from model.tournament import Tournament


class Controller:
    """Main controller"""

    def __init__(self,view):

        #View
        self.view = view

    ###Set players attribute list for later use in save/load function###
    PLAYERVALUESLIST = ["family_name", "first_name", "birth_date", "birth_date", "rank" ]

    ###Set path to data folder and database for players and tournaments###
    DATAFOLDER = Path("Data")
    db = TinyDB( DATAFOLDER/'database.json')
    player_db = db.table('players')
    finished_tour_namentdb = db.table('finished_tournament')
    ongoing_tournament_db = db.table("ongoing_tournament")

    ###function to launch the program###

    def run(self):
        self.main_menu()

    ###Input check###

    def check_input_type(self, input):
        """check if input can be turned into integer"""
        try:
            int(input)
        except ValueError:
            self.view.incorrect_input()
            return False
        return True

    ### Save related function ###

    def clear_player_list(self):
        """clear the current  player database to avoid duplicate"""
        self.player_db.truncate()

    def save_player(self, player):
        """save a new player"""
        self.player_db.insert(player.serialize())

    def find_player_correspondance(self,player):
        """take a serialized player,check for correspondance in database and return it's index"""
        matching_player = Query()
        player_id = self.player_db.get(matching_player["family_name"] == player["family_name"]
        and matching_player["first_name"] == player["first_name"]
        and matching_player["birth_date"] == player["birth_date"]).doc_id
        return player_id

    def find_player_db_intersect_tournament(self,tournament):
        """take the list of players in a serialized tournament and return it with the player index (from the player database) instead of the full player infos"""
        intersect = []      
        serialized_tournament_players = tournament["list_of_players"]
        for player in serialized_tournament_players:
            player_index = self.find_player_correspondance(serialized_tournament_players[player])
            intersect.append({"tournament_player_index":serialized_tournament_players[player]["tournament_player_index"],
            "db_player_index":player_index,
            "player_score" : serialized_tournament_players[player]["tournament_score"]})
        return intersect

    def ready_tournament_for_save(self,tournament):
        """Takes tournament object,serialize it and replace list of player by shortened version for storage"""
        savable_tournament = tournament.serialize()
        savable_tournament["list_of_players"] = self.find_player_db_intersect_tournament(savable_tournament)
        return savable_tournament


    def save_ongoing_tournament(self, tournament,tournament_index):
        """save ongoing tournament"""
        tournament_to_save = self.ready_tournament_for_save(tournament)
        if tournament_index > len(self.load_ongoing_tournament()):
            self.ongoing_tournament_db.insert(tournament_to_save)
        else:
            self.ongoing_tournament_db.upsert(Document(tournament_to_save,doc_id=tournament_index))

    ###Load related function ###

    def load_player_db(self):
        """load player database as list"""
        return self.player_db.all()

    def load_ongoing_tournament(self):
        """load ongoing tournament databse as a list"""
        return self.ongoing_tournament_db.all()

    def get_player_info_value(self,player_key,value_key):
        """Turn a player key from database.json into the value of the player info
        Value keys:
        -"family_name
        -"first_name"
        -"birth_date"
        -"birth_date"
        -"rank" """
        player_info_value = self.player_db.all()[player_key][value_key]
        return player_info_value

    def load_all_player_info_values(self,player_key):
        """Turn a player key from database.json into player a list of infos"""
        player_values = []
        for values in self.PLAYERVALUESLIST:
            player_values.append(self.get_player_info_value(player_key,values))
        return player_values

    def load_player(self,player_key):
        """Return a player object from the database"""
        values = self.load_all_player_info_values(player_key)
        return Player(values[0],values[1],values[2],values[3],values[4])


    ###Related to displaying database info###

    def show_player_index_for_selection(self):
        """display a list of players index and their full name"""
        for index in range(len(self.load_player_db())):
            self.view.print_player_index_and_name(self.load_player(index).give_full_name(),index)

 ##Main Menu##
    ###Main menu interactions###

    def main_menu(self):
        answer = True
        while answer:
            self.view.main_menu_display()
            answer = self.view.ask_for_input()
            if answer == "1":
                self.tournament_loading_menu()
                self.tournament_menu()
            elif answer == "2":
                self.create_tournament()
            elif answer == "3":
                self.data_menu()
            elif answer == "4":
                print("Vous quittez le programme,au revoir")
                sys.exit()
            else:
                self.view.incorrect_input()
                self.main_menu()

    def data_menu(self):
        answer = True
        while answer:
            self.view.data_menu_display()
            answer = self.view.ask_for_input()
            if answer == "1":
                pass
            elif answer == "2":
                pass
            elif answer == "3":
                self.main_menu()
            else:
                self.view.incorrect_input()
                self.data_menu()

    ### Function relatives to creating a tournament in the menu###

    def name_tournament(self):
        name = self.view.ask_for_tournament_name()
        return name

    def set_place(self):
        place = self.view.ask_for_place()
        return place

    def set_date(self):
        date = self.view.ask_for_date()
        return date

    def set_time_controller(self):
        time = True
        while time:
            time = self.view.ask_time_controller()
            if time == "1":
                time = "Bullet"
            elif time == "2":
                time = "Blitz"
            elif time == "3":
                time = "Coup rapide"
            else:
                self.view.incorrect_input()
                self.set_time_controller()
            return time



    def check_player_index_existance(self):
        """take int from function and check if the int exist in data base,then return it if it does"""  
        player_index = self.view.select_player()
        if self.check_input_type(player_index):
            if int(player_index) == 0 or  int(player_index) > len(self.load_player_db()):
                print(f"Aucun joueur n'a l'index n°:{player_index}\n"
                "Veuillez rentrer une nouvelle valeur\n")
                player_index = self.check_player_index_existance()
            else:
                return int(player_index)
        else:
            player_index = self.check_player_index_existance()

    def get_players(self):
        """select 8 players from players in database """
        players = []
        while len(players) < 8:
            if None in players:
                players.remove(None)
            self.show_player_index_for_selection()
            player_index = self.check_player_index_existance() 
            if player_index in players:
                print("Le joueur est déjà présent dans la liste,veuillez ajouter un autre joueur \n")
            elif player_index not in players:
                players.append(player_index)
            print("Index des joueurs déjà selectionés:\n")
            print(players)
        print("Liste des joueurs complète!\n"
        "Voici les joueurs selectionés:\n")
        for player in players:
            print(str(self.load_player(player - 1 ))) #Substract one to match db as list starting from 0
        print("souhaitez vous créer un tournois avec ces joueurs?\n")
        answer = self.view.confirmation()
        if answer == 'y':
            loaded_players = []
            for player in players:
                loaded_players.append(self.load_player(player -1))
            tournament_player_index = 1
            for loaded_player in loaded_players:
                    loaded_player.initialize_tournament_score()
                    loaded_player.initialize_tournament_player_index(tournament_player_index)
                    tournament_player_index += 1
            player_list = Playerlist(loaded_players)
            print("Les joueurs selectionnés sont:\n")
            print(player_list)
            return player_list
        elif answer == "n":
            self.get_players()

    def create_tournament(self):
        tournament = {}
        tournament["name"] = self.view.ask_for_tournament_name()
        tournament["place"] = self.view.ask_for_place()
        tournament["date"] = self.view.ask_for_date()
        tournament["players"] = self.get_players()
        tournament["time"] = self.set_time_controller()
        tournament["description"] = self.view.ask_for_description()
        print("Souhaitez vous créer un tournois avec les paramètres suivants?")
        for key in tournament:
            print( str(key) + " :" + str(tournament[key]) + "\n")
        confirmation = self.view.confirmation()
        if confirmation == "y":
            print("Création du tournois")
            tournament_index = len(self.load_ongoing_tournament()) +1
            print(f"Sauvegardé en tant que tournois n°{tournament_index}\n"
            "Chargez le tournois pour intéragir avec")
            new_tournament = Tournament(
                tournament["name"],
                tournament["place"],
                tournament["date"],
                tournament["players"],
                tournament["time"],
                tournament["description"]
            )              
            self.save_ongoing_tournament(new_tournament,tournament_index)
            self.main_menu()
        elif confirmation == "n":
            print("Vous allez retourner au menu principal\n"
            "Veuillez confirmer?`n")
            choice = self.view.confirmation()
            if choice == "n":
                print("Création du tournois")
                tournament_index = len(self.load_ongoing_tournament()) +1
                print(f"Sauvegardé en tant que tournois n°{tournament_index}\n"
                "Chargez le tournois pour intéragir avec")
                new_tournament = Tournament(
                    tournament["name"],
                    tournament["place"],
                    tournament["date"],
                    tournament["players"],
                    tournament["time"],
                    tournament["description"]
                )
                self.save_ongoing_tournament(new_tournament,tournament_index)
                self.main_menu()
            elif choice == "y":
                self.main_menu()
        
    ###Relative to loading an ongoing tournament"""

    def tournament_loading_menu(self):
        self.view.display_ongoing_tournament_list(self.load_ongoing_tournament())
        tournament_index = self.check_tournament_index_existance()
        tournament_dict = self.ongoing_tournament_db.get(doc_id=tournament_index)
        tournament_name = tournament_dict["tournament_name"]
        place = tournament_dict["place"]
        dates = tournament_dict["dates"]
        players = []
        for tournament_player in tournament_dict["list_of_players"]:
            player = self.load_player(tournament_player["db_player_index"] -1) #substract 1 to match document as list starting from 0
            player.set_tournament_index(tournament_player["tournament_player_index"])
            player.set_tournament_score(tournament_player["player_score"])
            players.append(player)
        playerlist = Playerlist(players)
        time_control = tournament_dict["time_control"]
        description = tournament_dict["description"]
        number_of_round = tournament_dict["number_of_rounds"]
        list_of_rounds = self.load_tournament_list_of_rounds(tournament_dict,players)
        loaded_tournament = Tournament(tournament_name, place, dates, playerlist, time_control, description, number_of_round,list_of_rounds)
        self.tournament = loaded_tournament
        self.current_tournament_index = tournament_index
        return self.tournament,self.current_tournament_index

    def load_match_list(self,round_dict,generated_players):
        match_list = []
        match_list_dict = round_dict["round_match_list"]
        generated_players_sorted = sorted(generated_players, key=lambda player: player.tournament_player_index)
        if round_dict["round_status"] == "Finished":
            for match in range(len(match_list_dict.keys())):
                for player in range(len(generated_players_sorted)):
                    if generated_players_sorted[player].tournament_player_index == match_list_dict[f"match n{match + 1}"][0][0]:
                        first_player = generated_players_sorted[player]
                for player in range(len(generated_players_sorted)):
                    if generated_players_sorted[player].tournament_player_index == match_list_dict[f"match n{match + 1}"][1][0]:
                        second_player = generated_players_sorted[player]
                match_object = Match(first_player,second_player)
                if match_list_dict[f"match n{match + 1}"][0][1] == "Victory":
                    match_object.set_result(1)
                elif match_list_dict[f"match n{match + 1}"][0][1] == "Defeat":
                    match_object.set_result(2)
                elif match_list_dict[f"match n{match + 1}"][0][1] == "Draw":
                    match_object.set_result(3)
                match_list.append(match_object)
        else:
            for match in range(len(match_list_dict.keys())):
                for player in range(len(generated_players_sorted)):
                    if generated_players_sorted[player].tournament_player_index == match_list_dict[f"match n{match + 1}"]["first_player"]:
                        first_player = generated_players_sorted[player]
                for player in range(len(generated_players_sorted)):
                    if generated_players_sorted[player].tournament_player_index == match_list_dict[f"match n{match + 1}"]["second_player"]:
                        second_player = generated_players_sorted[player]
                match_list.append(Match(first_player,second_player))
        return match_list




    def load_tournament_list_of_rounds(self,tournament_dict,generated_players):
        list_of_rounds = []
        rounds = tournament_dict["list_of_rounds"]
        for round in range(len(rounds)):
            if rounds[round]["round_status"] == "Finished":
                round_object = Round(rounds[round]["round_name"],
                "Finished",
                self.load_match_list(rounds[round],generated_players))
                round_object.set_start_time(rounds[round]["round_start_time"])
                round_object.set_end_time(rounds[round]["round_end_time"])
                list_of_rounds.append(round_object)        
            elif rounds[round]["round_status"] == "Started":
                round_object = Round(
                    rounds[round]["round_name"],
                    "Started",
                    self.load_match_list(rounds[round],generated_players)
                )
                round_object.set_start_time(rounds[round]["round_start_time"])
                list_of_rounds.append(round_object)
            elif rounds[round]["round_status"] == "Generated":
                list_of_rounds.append(Round(
                    rounds[round]["round_name"],
                    "Generated",
                    self.load_match_list(rounds[round],generated_players)
                ))
            elif rounds[round]["round_status"] == "Ungenerated":
                list_of_rounds.append(Round(rounds[round]["round_name"]))
        return list_of_rounds


    def check_tournament_index_existance(self):
        """take int from function and check if the int exist in data base,then return it if it does"""  
        tournament_index = self.view.ask_for_tournament_to_load()
        if self.check_input_type(tournament_index) is True:
            if int(tournament_index)==0 or int(tournament_index) >len(self.load_ongoing_tournament()):
                print(f"Aucun tournois n'a l'index n°:{tournament_index}\n"
                "Veuillez rentrer une nouvelle valeur\n")
                self.check_tournament_index_existance()
            else:
                return int(tournament_index)
        else:
            tournament_index = self.check_tournament_index_existance()

 ###Tournament controller###

    def tournament_menu(self):
        answer = True
        while answer:
            self.view.tournament_menu_display()
            answer = self.view.ask_for_input()
            if self.check_input_type(answer):
                if int(answer) == 1:
                    print(self.tournament.playerlist)
                elif int(answer) == 2:
                    self.view.tournament_status(self.tournament.list_of_rounds)
                elif int(answer) == 3:
                    for round_index in range(len(self.tournament.list_of_rounds)):
                        if self.tournament.list_of_rounds[round_index].status != "Finished":
                            self.round_menu(round_index)
                elif int(answer) == 4:
                    self.save_ongoing_tournament(self.tournament,self.current_tournament_index)
                    self.main_menu()
            elif self.check_input_type(answer) is False:
                self.view.incorrect_input()
                self.tournament_menu()

    def first_round_matchmaking(self):
        """divide the player list according to rank and create match pairing 
        opponants of each list according to ranl index"""
        match_list = []
        weakest_half = self.tournament.playerlist.get_weakest_half()
        strongest_half = self.tournament.playerlist.get_strongest_half()
        for player in strongest_half.playerlist:
            player_index = strongest_half.playerlist.index(player)
            match = Match(weakest_half.playerlist[player_index],strongest_half.playerlist[player_index])
            match_list.append(match)
        self.tournament.list_of_rounds[0].match_list = match_list



    def round_menu(self,round_index):
        answer = True
        while answer:
            self.view.round_menu_display(round_index)
            self.view.round_chronometer_display(self.tournament.list_of_rounds[round_index])
            answer = self.view.ask_for_input()
            if self.check_input_type(answer):
                if int(answer) == 1:
                    if self.tournament.list_of_rounds[round_index].match_list == []:
                        print("Les pairs n'ont pas encore été générée,"
                        " Veuillez choisir l'option 2")
                    else:
                        self.view.display_round_match_list(self.tournament.list_of_rounds[round_index])
                elif int(answer) == 2:
                    if self.tournament.list_of_rounds[round_index].match_list != []:
                        print("Les pair de joueurs ont déjà été généré,"
                        "Vous pouvez démarrer le round en préssant l'option 3 dans le menu du round")
                    else:
                        if round_index == 0:
                            self.first_round_matchmaking()
                            self.tournament.list_of_rounds[0].mark_match_as_generated()
                        else:
                            self.match_making()
                elif int(answer) == 3:
                    self.start_round(round_index)
                elif int(answer) == 4:
                    self.end_round(round_index)
                elif int(answer) == 5:
                    self.tournament_menu()
                elif int(answer) == 6:
                    self.save_ongoing_tournament(self.tournament,self.current_tournament_index)
                    self.main_menu()
            else:
                self.view.incorrect_input()
                self.round_menu(round_index)



    def end_round(self,round_index):
        if self.tournament.list_of_rounds[round_index].status == "Unplayed":
            self.view.error_end_not_started()
            self.round_menu(round_index)
        elif self.tournament.list_of_rounds[round_index].status == "Finished":
            self.view.error_end_already_ended()
            self.round_menu(round_index)
        elif self.tournament.list_of_rounds[round_index].status == "Started":
            self.view.end_round_confirmation()
            answer = self.view.ask_for_input()
            if answer.lower() == "y":
                self.tournament.list_of_rounds[round_index].end_round()
                for match in range(len(self.tournament.list_of_rounds[round_index].match_list)):
                    self.match_result(self.tournament.list_of_rounds[round_index].match_list[match])
            elif answer.lower() == "n":
                self.round_menu(round_index)
            else:
                self.view.incorrect_input()
                self.end_round(round_index)


    def start_round(self, round_index):
        if self.tournament.list_of_rounds[round_index].status == "Ungenerated":
            self.view.error_start_no_match_list()
            self.round_menu(round_index)
        elif self.tournament.list_of_rounds[round_index].status == "Finished":
            self.view.error_start_already_finished()
            self.round_menu(round_index)
        elif self.tournament.list_of_rounds[round_index].status == "Started":
            self.view.error_start_already_started()
        elif self.tournament.list_of_rounds[round_index].status == "Generated":
            self.view.start_round_confirmation()
            answer = self.view.ask_for_input()
            if answer.lower() == "y":
                self.tournament.list_of_rounds[round_index].start_round()
            elif answer.lower() == "n":
                self.round_menu(round_index)
            else:
                self.view.incorrect_input()
                self.start_round(round_index)

    def match_result(self,match):
        match_result = self.view.match_result_prompt(match)
        try:
            int(match_result)
        except ValueError:
            self.view.incorrect_input()
            self.match_result(match)
        else:
            if int(match_result) not in [1,2,3]:
                self.view.incorrect_input()
                self.match_result(match)
            elif int(match_result) == 1:
                match.first_player_victory()
                match.second_player_defeat()
                match.end_match()
            elif int(match_result) == 2:
                match.second_player_victory()
                match.first_player_defeat()
                match.end_match()
            elif int(match_result) == 3:
                match.first_player_draw()
                match.second_player_draw()
                match.end_match()
