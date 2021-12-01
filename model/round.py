#coding:utf-8

import time
from model.base import Base

@Base.register
class Round(Base):

    def __init__(self,
    name,
    status = "Ungenerated",
    match_list = []):
        super().__init__()
        self.name = name
        self.status = status
        self.match_list = match_list

    def mark_match_as_generated(self):
        self.status = "Generated"
        return self.status

    def start_round(self):
            self.status = "Started"
            self.start_time = time.time()
            print("Le chronomètre du tour a débuté")

    def end_round(self):
            self.status = "Finished"
            self.end_time = time.time()
            print("Le chronomètre du tour a pris fin.")

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_end_time(self,end_time):
        self.end_time = end_time

    def serialize(self):
        if self.status == "Ungenerated":
            serialized_round = {
                "round_name" : self.name,
                "round_status" : self.status,
                "round_match_list" : self.match_list
            }
            return serialized_round
        elif self.status == "Generated":
            serialized_match_list = {}
            for match in range(len(self.match_list)):
                serialized_match_list[f"match n{match+1}"] = self.match_list[match].serialize()
            serialized_round = {
                "round_name" : self.name,
                "round_status" : self.status,
                "round_match_list" : serialized_match_list
            }
            return serialized_round
        elif self.status == "Started":
            serialized_match_list = {}
            for match in range(len(self.match_list)):
                serialized_match_list[f"match n{match+1}"] = self.match_list[match].serialize()
            serialized_round = {
                "round_name" : self.name,
                "round_status" : self.status,
                "round_match_list" : serialized_match_list,
                "round_start_time" : self.start_time,                
            }
            return serialized_round
        elif self.status == "Finished":
            serialized_match_list = {}
            for match in range(len(self.match_list)):
                serialized_match_list[f"match n{match+1}"] = self.match_list[match].serialize()
            serialized_round = {
                "round_name" : self.name,
                "round_status" : self.status,
                "round_match_list" : serialized_match_list,
                "round_start_time" : self.start_time,
                "round_end_time" : self.end_time
            }
            return serialized_round
