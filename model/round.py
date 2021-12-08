# coding:utf-8

import time
from model.base import Base


class Round(Base):
    """round object"""

    def __init__(
        self,
        name,
        status="Ungenerated",
        match_list=[]
    ):
        """Create round object"""
        super().__init__()
        self.name = name
        self.status = status
        self.match_list = match_list

    def mark_match_as_generated(self):
        """mark round as generated once the matchmaking is called"""
        self.status = "Generated"
        return self.status

    def start_round(self):
        """mark round as started and create start time stamp"""
        self.status = "Started"
        self.start_time = time.time()
        print("Le chronomètre du tour a débuté")

    def end_round(self):
        """mark round as finished and create end time stamp"""
        self.status = "Finished"
        self.end_time = time.time()
        print("Le chronomètre du tour a pris fin.")

    def set_start_time(self, start_time):
        """set round start time when loading tournament"""
        self.start_time = start_time

    def set_end_time(self, end_time):
        """set round end time when loading tournament"""
        self.end_time = end_time

    def serialize_match_list(self):
        """turn each match in the list into a dictionnary to be added to serialized round"""
        serialized_match_list = {}
        for match in range(len(self.match_list)):
            serialized_match_list[f"match n{match+1}"] = self.match_list[match].serialize()
        return serialized_match_list

    def serialize_ungenerated(self):
        """turn ungenerated round into dictionnary savable into TinyDb"""
        serialized_round = {
            "round_name": self.name,
            "round_status": self.status,
            "round_match_list": self.match_list
        }
        return serialized_round

    def serialize_generated(self):
        """turn generated round into dictionnary savable into TinyDb"""
        serialized_match_list = self.serialize_match_list()
        serialized_round = {
            "round_name": self.name,
            "round_status": self.status,
            "round_match_list": serialized_match_list
        }
        return serialized_round

    def serialize_started(self):
        """turn startedd round into dictionnary savable into TinyDb"""
        serialized_match_list = self.serialize_match_list()
        serialized_round = {
            "round_name": self.name,
            "round_status": self.status,
            "round_match_list": serialized_match_list,
            "round_start_time": self.start_time,
        }
        return serialized_round

    def serialize_finished(self):
        """turn finished round into dictionnary savable into TinyDb"""
        serialized_match_list = self.serialize_match_list()
        serialized_round = {
            "round_name": self.name,
            "round_status": self.status,
            "round_match_list": serialized_match_list,
            "round_start_time": self.start_time,
            "round_end_time": self.end_time
        }
        return serialized_round

    def serialize(self):
        """turn round in dictionnary savable into TinyDb according to round status"""
        if self.status == "Ungenerated":
            return self.serialize_ungenerated()
        elif self.status == "Generated":
            return self.serialize_generated()
        elif self.status == "Started":
            return self.serialize_started()
        elif self.status == "Finished":
            return self.serialize_finished()
