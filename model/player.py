#coding:utf-8

from model.base import Base

@Base.register
class Player(Base):
    """Player object with full name,birthdate,gender and rank"""

    def __init__(self,
                 family_name,
                 first_name,
                 birth_date,
                 gender,
                 rank):
        super().__init__()
        self.family_name = family_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.rank = rank

    def initialize_tournament_score(self):
        self.tournament_score = 0
        return self.tournament_score

    def initialize_tournament_player_index(self,player_index):
        self.tournament_player_index = player_index
        return self.tournament_player_index

    def set_tournament_score(self,score):
        self.tournament_score = score
        return self.tournament_score

    def set_tournament_index(self,player_index):
        self.tournament_player_index = player_index
        return self.tournament_player_index


    def victory(self):
        self.tournament_score += 1
        return self.tournament_score

    def draw(self):
        self.tournament_score += 0.5
        return self.tournament_score

    def give_full_name(self):
        """return full player name"""
        full_name = f"{self.family_name} {self.first_name}"
        return full_name

    def serialize(self):
        serialized_player = {
            "family_name": self.family_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "rank": self.rank
        }
        try:
            self.tournament_score
        except AttributeError:
            pass
        else:
            serialized_player["tournament_score"] = self.tournament_score
        try:
            self.tournament_player_index
        except AttributeError:
            pass
        else:
            serialized_player["tournament_player_index"] = self.tournament_player_index
        return serialized_player


    def __dir__(self):
        """overide __dir__ to return those arguments"""
        return [
            self.family_name,
            self.first_name,
            self.birth_date,
            self.gender,
            self.rank
        ]

    def __str__(self):
        """used in print"""
        display = (f"\nJoueur: {self.give_full_name()} \n" \
            f"Date de naissance: {self.birth_date} \n" \
            f"Genre: {self.gender} \n" \
            f"Rang: {self.rank} \n")
        try:
            self.tournament_score
        except AttributeError:
            pass
        else:
            display += f"Score du tournois: {self.tournament_score}"
        return display

    def __repr__(self) -> str:
        return str(self)
