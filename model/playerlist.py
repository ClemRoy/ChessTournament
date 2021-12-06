#coding:utf-8

from model.base import Base

@Base.register
class Playerlist(Base):

    def __init__(self, playerlist:list ):
        super().__init__()
        """Create a player list"""
        self.playerlist = playerlist

    def serialize(self):
        serialized_player_list = {}
        for i in range(len(self.playerlist)):
            serialized_player_list[i] = self.playerlist[i].serialize()
        return serialized_player_list

    def printlist(self):
        """Display the list in it's current order"""
        print('Liste des Joueurs')
        for player in self.playerlist:
            player.__str__()

    def sort_playerlist_by_rank(self):
        """Sort the list from the weakest to the strongest rank"""
        new_player_list = self.playerlist
        new_player_list.sort(key=lambda player: player.rank)
        return new_player_list
        

    def sort_playerlist_by_score_and_rank(self):
        """return list of tournament player starting from the strongest"""
        new_player_list = self.playerlist
        new_player_list.sort(key=lambda player: (player.tournament_score, player.rank), reverse=True)
        return new_player_list

    def find_player_list_middle(self,list):
        """find the middle of the player list"""
        lenth = len(list)
        middle_index = lenth // 2
        return middle_index

    def get_weakest_half(self):
        """Give a player list made of the weakest part of this player list"""
        sorted_playerlist = self.sort_playerlist_by_rank()
        weakest_half = sorted_playerlist[:self.find_player_list_middle(sorted_playerlist)]
        return weakest_half

    def get_strongest_half(self):
        """Give a player list made of the strongest part of this player list"""
        sorted_playerlist = self.sort_playerlist_by_rank()
        strongest_half = sorted_playerlist[self.find_player_list_middle(sorted_playerlist):]
        return strongest_half

    def get_player_list_score(self):
        """Display the list of tournament player by tournament score"""
        sorted_by_tourn_score = self.sort_playerlist_by_score_and_rank()
        liste = "Liste des joueurs par index du tournois: \n"
        for player in sorted_by_tourn_score:
            liste += "\n" + str(player) + "\n"
        return liste

    def get_player_list(self):
        """Display the list of tournament player by tournament index"""
        sorted_by_tourn_index = sorted(self.playerlist, key=lambda player: player.tournament_player_index)
        liste = "Liste des joueurs par index du tournois: \n"
        for player in sorted_by_tourn_index:
            liste += "\n" + str(player) + "\n"
        return liste

    def __str__(self):
        return self.get_player_list()

    def __repr__(self) -> str:
        return str(self)    

