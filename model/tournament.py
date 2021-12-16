# coding:utf-8

from model.base import Base
from model.playerlist import Playerlist
from model.round import Round


class Tournament(Base):
    """Tournament object"""

    def __init__(
        self,
        tournament_name,
        place,
        dates,
        list_of_players: Playerlist,
        time_control,
        description,
        number_of_rounds=4,
        list_of_rounds=[]
            ):
        """Create tournament object"""
        super().__init__()
        self.tournament_name = tournament_name
        self.place = place
        self.dates = dates
        self.number_of_round = number_of_rounds
        self.playerlist = list_of_players
        self.time_control = time_control
        self.description = description
        self.list_of_rounds = list_of_rounds
        if list_of_rounds == []:
            for round in range(self.number_of_round):
                round_name = f"Round {round + 1}"
                self.list_of_rounds.append(Round(round_name))
        self.already_played_match = []
        self.generate_played_match_list()

    def generate_played_match_list(self):
        if self.list_of_rounds[0].status == "Ungenerated":
            pass
        else:
            for round_index in range(len(self.list_of_rounds)):
                self.refresh_played_match_list(round_index)

    def refresh_played_match_list(self,round_index):
        if self.list_of_rounds[round_index].status != "Ungenerated":
            for match in range(len(self.list_of_rounds[round_index].match_list)):
                played_match = self.list_of_rounds[round_index].match_list[match]
                match_for_list = [played_match.first_player.tournament_player_index,
                played_match.second_player.tournament_player_index]
                match_for_list.sort()
                if match_for_list not in self.already_played_match:
                    self.already_played_match.append(match_for_list)

    def serialize(self):
        """transform tournament into dictionary savable in Tinydb"""
        serialized_ongoing_tournament = {
            "tournament_name": self.tournament_name,
            "place": self.place,
            "dates": self.dates,
            "list_of_players": self.playerlist.serialize(),
            "time_control": self.time_control,
            "description": self.description,
            "number_of_rounds": self.number_of_round,
            "list_of_rounds": []
        }
        for round in range(len(self.list_of_rounds)):
            serialized_ongoing_tournament["list_of_rounds"].append(self.list_of_rounds[round].serialize())
        return serialized_ongoing_tournament
