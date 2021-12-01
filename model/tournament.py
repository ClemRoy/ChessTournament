#coding:utf-8

from model.base import Base
from model.playerlist import Playerlist
from model.round import Round

@Base.register
class Tournament(Base):

    def __init__(
        self,
        tournament_name,
        place,
        dates,
        list_of_players:Playerlist,
        time_control,
        description,
        number_of_rounds = 4,
        list_of_rounds = []
        ):
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


    def save_round(self, round):
        self.list_of_rounds.append(round)


    def serialize(self):
        serialized_ongoing_tournament = {
            "tournament_name": self.tournament_name,
            "place": self.place,
            "dates": self.dates,
            "list_of_players":self.playerlist.serialize(),
            "time_control": self.time_control,
            "description": self.description,
            "number_of_rounds": self.number_of_round,
            "list_of_rounds" : []
        }
        for round in range(len(self.list_of_rounds)):
            serialized_ongoing_tournament["list_of_rounds"].append(self.list_of_rounds[round].serialize())
        return serialized_ongoing_tournament