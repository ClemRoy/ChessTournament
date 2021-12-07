#coding:utf-8
"""match object"""

from model.base import Base
from model.player import Player

@Base.register
class Match():
    """Match object"""

    def __init__(self, first_player:Player, second_player:Player):
        """create match object"""
        self.first_player = first_player
        self.second_player = second_player
        self.match_status = "Unplayed"

    def apply_result(self,result):
        """apply player input to set match result
        (1=1st player victory,2=2nd player victory,3=Draw)"""
        if result == 1:
            self.first_player_victory()
            self.second_player_defeat()
        elif result == 2:
            self.second_player_victory()
            self.first_player_defeat()
        elif result == 3:
            self.first_player_draw()
            self.second_player_draw()
        self.end_match()
        
    def first_player_victory(self):
        """apply first player victory"""
        self.first_player_result = "Victory"
        self.first_player.victory()
        return self.first_player_result
    
    def first_player_defeat(self):
        """apply first player defeat"""
        self.first_player_result = "Defeat"
        return self.first_player_result

    def first_player_draw(self):
        """apply draw to first player"""
        self.first_player_result = "Draw"
        self.first_player.draw()
        return self.first_player_result

    def second_player_victory(self):
        """apply second player victory"""
        self.second_player_result = "Victory"
        self.second_player.victory()
        return self.second_player_result

    def second_player_defeat(self):
        """apply second player defeat"""
        self.second_player_result = "Defeat"
        return self.second_player_result

    def second_player_draw(self):
        """apply draw to second player"""
        self.second_player_result = "Draw"
        self.second_player.draw()
        return self.second_player_result
        
    def start_match(self):
        """set match status as started"""
        self.match_status = "Started"
        return self.match_status

    def end_match(self):
        """set match status as finished"""
        self.match_status = "Finished"
        return self.match_status

    def set_result(self,result):
        """set match result when loading tournament"""
        if result == 1:
            self.first_player_result = "Victory"
            self.second_player_result = "Defeat"
            self.end_match()
        elif result == 2:
            self.first_player_result = "Defeat"
            self.second_player_result = "Victory"
            self.end_match()
        elif result == 3:
            self.first_player_result = "Draw"
            self.second_player_result = "Draw"
            self.end_match()



    def serialize(self):
        if self.match_status == "Unplayed":
            serialized_match = {
            "first_player": self.first_player.tournament_player_index,
            "second_player": self.second_player.tournament_player_index,
            "match_status": self.match_status
        }
        elif self.match_status == "Finished":
            serialized_match = ( [self.first_player.tournament_player_index,self.first_player_result],
            [self.second_player.tournament_player_index,self.second_player_result]
            )
        return serialized_match

    def __str__(self):
        """used in print"""
        display = ("\nMatch opposant:\n"
        f"{self.first_player.give_full_name()}\n"
        "contre \n"
        f"{self.second_player.give_full_name()}\n")
        if self.match_status == "Unplayed":
            display += " Le match n'a pas été joué\n"
        elif self.match_status == "Finished":
            display += ("Le match est terminé \n")
            if self.first_player_result == "Victory":
                display += f"Victoire de {self.first_player.give_full_name()}\n"
            elif self.first_player_result == "Defeat":
                display += f"Victoire de {self.second_player.give_full_name()}\n"
            elif self.first_player_result == "Draw":
                display += "Match nul\n"            
        return display

    
    def __repr__(self) -> str:
        return str(self)