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

    def sortplayerlist(self):
        """Sort the list from the weakest to the strongest rank"""
        self.playerlist = sorted(self.playerlist, key=lambda player: player.rank)

    def find_player_list_middle(self):
        """find the middle of the player list"""
        lenth = len(self.playerlist)
        middle_index = lenth // 2
        return middle_index

    def get_weakest_half(self):
        """Give a player list made of the weakest part of this player list"""
        self.sortplayerlist()
        self.weakest_half = self.playerlist[:self.find_player_list_middle()]
        return Playerlist(self.weakest_half)

    def get_strongest_half(self):
        """Give a player list made of the strongest part of this player list"""
        self.sortplayerlist()
        self.strongest_half = self.playerlist[self.find_player_list_middle():]
        return Playerlist(self.strongest_half)

    def get_player_list(self):
        """Display the list of tournament player by tournament index"""
        sorted_by_tourn_index = sorted(self.playerlist, key=lambda player: player.tournament_player_index)
        liste = "Liste des joueurs: \n"
        for player in sorted_by_tourn_index:
            liste += "\n" + str(player) + "\n"
        return liste

    def __str__(self):
        return self.get_player_list()

    def __repr__(self) -> str:
        return str(self)    

