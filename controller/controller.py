#coding:utf-8

from os import system
import sys
from pathlib import Path
from tinydb import TinyDB
from tinydb.queries import Query
from tinydb.table import Document
from tinydb.utils import V
from model.player import Player
from model.playerlist import Playerlist
from model.match import Match
from model.round import Round
from model.tournament import Tournament


class Controller:
    """Main controller"""

    def __init__(self,view):
        """create controller object"""

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
        """return True if input can be turned into integer"""
        try:
            int(input)
        except ValueError:
            self.view.incorrect_input()
            return False
        return True

    ### Save related function ###

    def save_player(self, player):
        """save a new player at the end of the player database"""
        self.player_db.insert(player.serialize())

    def find_player_correspondance(self,player):
        """take a serialized player,check for correspondance in database and return it's index"""
        matching_player = Query()
        player_id = self.player_db.get(matching_player["family_name"] == player["family_name"]
        and matching_player["first_name"] == player["first_name"]
        and matching_player["birth_date"] == player["birth_date"]).doc_id
        return player_id

    def find_player_db_intersect_tournament(self,tournament):
        """take the list of players in a serialized tournament and return it with
         the player index (from the player database) instead of the full player infos"""
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
        self.ongoing_tournament_db.upsert(Document(tournament_to_save,doc_id=tournament_index))

    def save_finished_tournament(self,tournament):
        """Remove finished tournament from ongoing tournament database and 
        save it in finished tournament database,
        display the index at witch it is saved and return to main menu"""
        tournament_index = len(self.load_finished_tournament()) + 1
        tournament_to_save = self.ready_tournament_for_save(tournament)
        self.ongoing_tournament_db.remove(doc_ids=[self.current_tournament_index])
        self.finished_tour_namentdb.insert(tournament_to_save)
        self.view.tournament_is_over(tournament_index)
        self.main_menu()

    ###Load related function ###

    def load_player_db(self):
        """retun player database as list"""
        return self.player_db.all()

    def load_ongoing_tournament(self):
        """return ongoing tournament databse as a list"""
        return self.ongoing_tournament_db.all()

    def load_finished_tournament(self):
        """return finished tournaments as a list"""
        return self.finished_tour_namentdb.all()

    def get_player_info_value(self,player_key,value_key):
        """Turn a player key from database.json into the value of the player info
        Value keys:
        \n-"family_name
        \n-"first_name"
        \n-"birth_date"
        \n-"birth_date"
        \n-"rank" """
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
        """Display main menu"""
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
        """Display menu to interact with data"""
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
        """get input for tournament name"""
        name = self.view.ask_for_tournament_name()
        return name

    def set_place(self):
        """Get input for tournament place"""
        place = self.view.ask_for_place()
        return place

    def set_date(self):
        """Get input for tournament date"""
        date = self.view.ask_for_date()
        return date

    def set_time_controller(self):
        """Get input for time controller setting"""
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
        """take int from function and check if the int match
        an index in player database,then return it if it does"""  
        player_index = self.view.select_player()
        if self.check_input_type(player_index):
            if int(player_index) == 0 or  int(player_index) > len(self.load_player_db()):
                self.view.incorrect_player_index(player_index)
                player_index = self.check_player_index_existance()
            else:
                return int(player_index)
        else:
            player_index = self.check_player_index_existance()

    def add_player(self):
        """establish the tournament playerlist"""
        players = []
        while len(players) < 8:
            self.show_player_index_for_selection()
            player_index = self.check_player_index_existance() 
            if player_index in players:
                print("Le joueur est déjà présent dans la liste,veuillez ajouter un autre joueur \n")
            elif player_index == None:
                pass
            elif player_index not in players:
                players.append(player_index)
            self.view.display_selected_players(players)
        return players

    def load_players(self,players):
        loaded_players = []
        for player in players:
            loaded_players.append(self.load_player(player -1)) #Substract one to match db as list starting from 0
        return loaded_players

    def initialize_players(self,loaded_players):
        player_to_initialize = loaded_players
        tournament_player_index = 1
        for loaded_player in player_to_initialize:
            loaded_player.initialize_tournament_score()
            loaded_player.initialize_tournament_player_index(tournament_player_index)
            tournament_player_index += 1
        return player_to_initialize


    def get_players(self):
        """select 8 players from players in database """
        players = self.add_player()
        loaded_players = self.load_players(players)
        self.view.player_selection_list_full(loaded_players)
        answer = self.view.confirmation()
        if answer == 'y':
            initialized_players = self.initialize_players(loaded_players)
            player_list = Playerlist(initialized_players)
            return player_list
        elif answer == "n":
            self.get_players()

    def get_tournament_info(self):
        tournament = {}
        tournament["name"] = self.view.ask_for_tournament_name()
        tournament["place"] = self.view.ask_for_place()
        tournament["date"] = self.view.ask_for_date()
        tournament["players"] = self.get_players()
        tournament["time"] = self.set_time_controller()
        tournament["description"] = self.view.ask_for_description()
        return tournament

    def turn_tourn_dict_into_object(self, tournament_dict):
        tournament = tournament_dict
        new_tournament = Tournament(
                tournament["name"],
                tournament["place"],
                tournament["date"],
                tournament["players"],
                tournament["time"],
                tournament["description"],
                )
        return new_tournament

    def save_new_tournament(self, tournament_dict):
        saved_tournament_index_list = []
        for document in self.load_ongoing_tournament():
            saved_tournament_index = document.doc_id
            saved_tournament_index_list.append(saved_tournament_index)
        max_possible_index = len(saved_tournament_index_list) + 2
        for possible_index in range(1,max_possible_index):
            if possible_index not in saved_tournament_index_list:
                tournament_index = possible_index
                self.view.tournament_creation_display(tournament_index)
                new_tournament = self.turn_tourn_dict_into_object(tournament_dict)
                self.save_ongoing_tournament(new_tournament,tournament_index)
                self.main_menu()

    def create_tournament(self):
        tournament_dict = self.get_tournament_info()
        self.view.tournament_creation_confirmation(tournament_dict)
        confirmation = self.view.confirmation()
        if confirmation == "y":
            self.save_new_tournament(tournament_dict)
        elif confirmation == "n":
            self.view.return_to_menu_confirmation()
            choice = self.view.confirmation()
            if choice == "n":
                self.save_new_tournament(tournament_dict)
            elif choice == "y":
                self.main_menu()
        
    ###Relative to loading an ongoing tournament"""

    def get_tournament_to_load_index(self):
        if self.load_ongoing_tournament() == []:
            self.view.no_ongoing_tournament()
            self.main_menu()
        self.view.display_ongoing_tournament_list(self.load_ongoing_tournament())
        tournament_index = self.check_tournament_index_existance()
        return tournament_index

    def turn_playerlist_dict_into_object(self,playerlist):
        players = []
        for tournament_player in playerlist:
            player = self.load_player(tournament_player["db_player_index"] -1) #substract 1 to match document as list starting from 0
            player.set_tournament_index(tournament_player["tournament_player_index"])
            player.set_tournament_score(tournament_player["player_score"])
            players.append(player)
        playerlist = Playerlist(players)
        return playerlist


    def turn_saved_tournament_into_object(self,tournament_to_load_index):
        tournament_index = tournament_to_load_index
        tournament_dict = self.ongoing_tournament_db.get(doc_id=tournament_index)
        tournament_name = tournament_dict["tournament_name"]
        place = tournament_dict["place"]
        dates = tournament_dict["dates"]
        playerlist = self.turn_playerlist_dict_into_object(tournament_dict["list_of_players"])
        players = playerlist.playerlist
        time_control = tournament_dict["time_control"]
        description = tournament_dict["description"]
        number_of_round = tournament_dict["number_of_rounds"]
        list_of_rounds = self.load_tournament_list_of_rounds(tournament_dict,players)
        loaded_tournament = Tournament(tournament_name, place, dates, playerlist, time_control, description, number_of_round,list_of_rounds)
        return loaded_tournament


    def tournament_loading_menu(self):
        tournament_index = self.get_tournament_to_load_index()
        loaded_tournament = self.turn_saved_tournament_into_object(tournament_index)
        self.tournament = loaded_tournament
        self.current_tournament_index = tournament_index
        return self.tournament,self.current_tournament_index





    def load_match_list(self,round_dict,generated_players):
        match_list = []
        match_list_dict = round_dict["round_match_list"]  
        generated_players_sorted = generated_players
        generated_players_sorted.sort(key=lambda player: player.tournament_player_index)
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
        elif round_dict["round_status"] == "Started":
            for match in range(len(match_list_dict.keys())):
                for player in range(len(generated_players_sorted)):
                    if generated_players_sorted[player].tournament_player_index == match_list_dict[f"match n{match + 1}"]["first_player"]:
                        first_player = generated_players_sorted[player]
                for player in range(len(generated_players_sorted)):
                    if generated_players_sorted[player].tournament_player_index == match_list_dict[f"match n{match + 1}"]["second_player"]:
                        second_player = generated_players_sorted[player]
                match_object = Match(first_player,second_player)
                match_object.start_match()
                match_list.append(match_object)
        elif round_dict["round_status"] == "Generated":
            for match in range(len(match_list_dict.keys())):
                for player in range(len(generated_players_sorted)):
                    if generated_players_sorted[player].tournament_player_index == match_list_dict[f"match n{match + 1}"]["first_player"]:
                        first_player = generated_players_sorted[player]
                for player in range(len(generated_players_sorted)):
                    if generated_players_sorted[player].tournament_player_index == match_list_dict[f"match n{match + 1}"]["second_player"]:
                        second_player = generated_players_sorted[player]
                match_list.append(Match(first_player,second_player))
        elif round_dict["round_status"] == "Ungenerated":
            pass
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
        current_ongoing_tournaments_index = []
        ongoing_tournament = self.load_ongoing_tournament()
        for documents in range(len(ongoing_tournament)):
            current_ongoing_tournaments_index.append(ongoing_tournament[documents].doc_id)
        tournament_index = self.view.ask_for_tournament_to_load()
        while self.check_input_type(tournament_index) is not True:
            tournament_index = self.view.ask_for_tournament_to_load()
        while int(tournament_index) not in current_ongoing_tournaments_index:
            print(f"Aucun tournois n'a l'index n°:{tournament_index}\n"
            "Veuillez rentrer une nouvelle valeur\n")
            tournament_index = self.view.ask_for_tournament_to_load()          
        return int(tournament_index)


 ###Tournament controller###

    def tournament_menu(self):
        answer = True
        while answer:
            self.view.tournament_menu_display()
            answer = self.view.ask_for_input()
            if self.check_input_type(answer):
                if int(answer) == 1:
                    display_choice = self.view.player_list_display_choice()
                    if self.check_input_type(display_choice) is True:
                        if int(display_choice) in [1,2]:
                            if int(display_choice) == 1:
                                print(self.tournament.playerlist)
                            elif int(display_choice) == 2:
                                print(self.tournament.playerlist.get_player_list_score())
                        else:
                            self.view.incorrect_input()
                            display_choice = self.view.player_list_display_choice()
                    else:
                        self.view.incorrect_input()
                        display_choice = self.view.player_list_display_choice()
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
        for player in strongest_half:
            player_index = strongest_half.index(player)
            match = Match(weakest_half[player_index],strongest_half[player_index])
            match_list.append(match)
        self.tournament.list_of_rounds[0].match_list = match_list
        self.tournament.list_of_rounds[0].mark_match_as_generated()
        self.tournament.refresh_played_match_list(0)


    def round_menu(self,round_index):
        answer = True
        while answer:
            self.view.round_menu_display(round_index)
            self.view.round_chronometer_display(self.tournament.list_of_rounds[round_index])
            answer = self.view.ask_for_input()
            if self.check_input_type(answer):
                if int(answer) == 1:
                    if self.tournament.list_of_rounds[round_index].status == "Ungenerated":
                        print("Les pairs n'ont pas encore été générée,"
                        " Veuillez choisir l'option 2")
                    else:
                        self.view.display_round_match_list(self.tournament.list_of_rounds[round_index])
                elif int(answer) == 2:
                    if self.tournament.list_of_rounds[round_index].status != "Ungenerated":
                        print("Les pair de joueurs ont déjà été généré,"
                        "Vous pouvez démarrer le round en préssant l'option 3 dans le menu du round")
                    else:
                        if round_index == 0:
                            self.first_round_matchmaking()
                            self.save_ongoing_tournament(self.tournament,self.current_tournament_index)
                        else:
                            self.match_making1(round_index)
                            self.save_ongoing_tournament(self.tournament,self.current_tournament_index)
                elif int(answer) == 3:
                    self.start_round(round_index)
                    self.save_ongoing_tournament(self.tournament,self.current_tournament_index)
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


    def get_sorted_players_idx(self):
        """return a list of players index,from the highest score/rank to the lowest"""
        new_list =  self.tournament.playerlist.sort_playerlist_by_score_and_rank()
        return [el.tournament_player_index for el in new_list]


    def get_duo_for_first_player(self, sorted_players):
        print("sorted_players in get duo")
        print(sorted_players)
        if len(sorted_players) < 2:
            print("I shouldn't be here")
        elif len(sorted_players) == 2 and  not self._did_players_never_played(sorted_players[0], sorted_players[1]):
            print("I'm here,no other player to pair")
            first_player = sorted_players[0]
            second_player = sorted_players[1]
            print(first_player,second_player)
            return {"1":first_player , "2": second_player }
        else:
            if self._did_players_never_played(sorted_players[0], sorted_players[1]):
                print("I'm here,the player never played together and are added")
                first_player = sorted_players[0]
                second_player = sorted_players[1]
                print(first_player,second_player)
                return {"1":first_player , "2": second_player }
            elif not self._did_players_never_played(sorted_players[0],sorted_players[1]):
                print("I'm here,the players already played together")
                sorted_players.remove(sorted_players[1])
                return self.get_duo_for_first_player(sorted_players )
                
    def _did_players_never_played(self, idx_player1, idx_player2):
        potential_match = [idx_player1,idx_player2]
        potential_match.sort()
        if potential_match in self.tournament.already_played_match:
            return False
        else:
            return True


    def match_tournament_index_with_player_object(self,tournament_index):
        for player in self.tournament.playerlist.playerlist:
            if player.tournament_player_index == tournament_index:
                return player

    def turn_match_dict_into_match_obj(self,match_dictionnary):
        first_player_index = list(match_dictionnary.keys())[0]
        first_player = self.match_tournament_index_with_player_object(first_player_index)
        second_player_index = list(match_dictionnary.values())[0]
        second_player = self.match_tournament_index_with_player_object(second_player_index)
        return Match(first_player,second_player)

    def get_match_dict(self,round_playerlist_index):
        next_matchs_dict = []
        for player_index,_ in enumerate(round_playerlist_index):
            new_match_tmp = self.get_duo_for_first_player(round_playerlist_index[player_index:])
            new_match = {new_match_tmp["1"]: new_match_tmp["2"]}
            next_matchs_dict.append(new_match)
            round_playerlist_index.remove(new_match_tmp["2"])
            if None in next_matchs_dict:
                next_matchs_dict.remove(None)
        return next_matchs_dict



    def match_making1(self,round_index):
        """generate a list of previous matchs,get a list of players
         indexs sorted from the strongest to the weakest"""
        print(self.tournament.already_played_match)
        next_round_matchs = []
        round_playerlist_index = self.get_sorted_players_idx()
        next_matchs_dict = self.get_match_dict(round_playerlist_index)
        print("I'm here match_making1")
        print(next_matchs_dict)
        for match in next_matchs_dict:
            next_round_matchs.append(self.turn_match_dict_into_match_obj(match))
        self.tournament.list_of_rounds[round_index].match_list = next_round_matchs
        self.tournament.list_of_rounds[round_index].mark_match_as_generated()
        self.tournament.refresh_played_match_list(round_index)

    def end_round(self,round_index):
        """check round status to see if round can be ended,then call function to end it if it can"""
        if self.tournament.list_of_rounds[round_index].status == "Ungenerated":
            self.view.error_end_not_generated()
            self.round_menu(round_index)
        elif self.tournament.list_of_rounds[round_index].status == "Generated":
            self.view.error_end_not_started()
            self.round_menu(round_index)
        elif self.tournament.list_of_rounds[round_index].status == "Finished":
            self.view.error_end_already_ended()
            self.round_menu(round_index)
        elif self.tournament.list_of_rounds[round_index].status == "Started":
            self.end_round_correct(round_index)

    def end_round_correct(self, round_index):
        """ask for confirmation then mark round as finished,create end time stamp,
        and call next round menu or save tournament if finished"""
        self.view.end_round_confirmation()
        answer = self.view.ask_for_input()
        if answer.lower() == "y":
            self.tournament.list_of_rounds[round_index].end_round()
            for match in range(len(self.tournament.list_of_rounds[round_index].match_list)):
                self.match_result(self.tournament.list_of_rounds[round_index].match_list[match])
            if round_index + 1 == len(self.tournament.list_of_rounds):
                self.save_finished_tournament(self.tournament)
            else:
                self.save_ongoing_tournament(self.tournament,self.current_tournament_index)
                self.tournament.refresh_played_match_list(round_index)
                self.round_menu(round_index + 1)
        elif answer.lower() == "n":
            self.round_menu(round_index)
        else:
            self.view.incorrect_input()
            self.end_round(round_index)  


    def start_round(self, round_index):
        """check round status before calling funct to start round if it can be"""
        if self.tournament.list_of_rounds[round_index].status == "Ungenerated":
            self.view.error_start_no_match_list()
            self.round_menu(round_index)
        elif self.tournament.list_of_rounds[round_index].status == "Finished":
            self.view.error_start_already_finished()
            self.round_menu(round_index)
        elif self.tournament.list_of_rounds[round_index].status == "Started":
            self.view.error_start_already_started()
            self.round_menu(round_index)
        elif self.tournament.list_of_rounds[round_index].status == "Generated":
            self.start_round_correct(round_index)


    def start_round_correct(self, round_index):
        """ask for confirmation then mark round as started and create start time stamp"""
        self.view.start_round_confirmation()
        answer = self.view.ask_for_input()
        if answer.lower() == "y":
            self.tournament.list_of_rounds[round_index].start_round()
        elif answer.lower() == "n":
            self.round_menu(round_index)
        else:
            self.view.incorrect_input()
            self.start_round(round_index)

    def first_player_victory(self,match):
        """Mark match as first player victory"""
        match.first_player_victory()
        match.second_player_defeat()
        match.end_match()

    def second_player_victory(self,match):
        """Mark match as second player victory"""
        match.second_player_victory()
        match.first_player_defeat()
        match.end_match()

    def draw(self,match):
        """Mark match as a draw"""
        match.first_player_draw()
        match.second_player_draw()
        match.end_match()

    def check_match_result_input(self,match):
        """Check if input for match resuslt can be an integer between 1 & 3"""
        match_result= self.view.match_result_prompt(match)
        if self.check_input_type(match_result):
            if int(match_result) in [1,2,3]:
                return int(match_result)
            else:
                return self.check_match_result_input(match)
        else:
            return self.check_match_result_input(match)

    def match_result(self,match):
        """Apply result to match according to input"""
        match_result = self.check_match_result_input(match)
        if int(match_result) == 1:
            self.first_player_victory(match)
        elif int(match_result) == 2:
            self.second_player_victory(match)
        elif int(match_result) == 3:
            self.draw(match)