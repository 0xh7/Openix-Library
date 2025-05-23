import json
import os
import random
from Openix import ChessOpening

class ChessOpeningsLibrary:
  

    def __init__(self):
        self.openings = {}

    def load_from_json_file(self, file_path):
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
     
        if isinstance(data, dict):
            for entry in data.values():
                if not isinstance(entry, dict):
                    continue
                opening = ChessOpening.from_dict(entry)
                if opening.eco_code and opening.moves_list:
                    self.openings[opening.eco_code] = opening
        elif isinstance(data, list):
            for entry in data:
                if not isinstance(entry, dict):
                    continue
                opening = ChessOpening.from_dict(entry)
                if opening.eco_code and opening.moves_list:
                    self.openings[opening.eco_code] = opening

    def load_multiple_files(self, files_list):
        for file_path in files_list:
            self.load_from_json_file(file_path)

    def find_by_eco(self, eco_code):
        return self.openings.get(eco_code)

    def search_by_name(self, name_substring):
        results = []
        for opening in self.openings.values():
            if name_substring.lower() in opening.name.lower():
                results.append(opening)
        return results

    def find_openings_starting_with(self, move_san):
       
        results = []
        for opening in self.openings.values():
            if opening.moves_list and opening.moves_list[0] == move_san:
                results.append(opening)
        return results

    def find_openings_after_moves(self, moves_list):
 
        results = []
        for opening in self.openings.values():
            if opening.moves_list[:len(moves_list)] == moves_list:
                results.append(opening)
        return results

    def get_random_opening(self):
     
        if not self.openings:
            return None
        return random.choice(list(self.openings.values()))

    def get_random_opening_starting_with(self, move_san):
   
        candidates = self.find_openings_starting_with(move_san)
        if not candidates:
            return None
        return random.choice(candidates)

    def get_random_opening_after_moves(self, moves_list):
    
        candidates = self.find_openings_after_moves(moves_list)
        if not candidates:
            return None
        return random.choice(candidates)

    def list_openings_after_moves(self, moves_list):
       
        return self.find_openings_after_moves(moves_list)

    def list_next_moves_after(self, moves_list):
     
        next_moves = {}
        for opening in self.openings.values():
            if opening.moves_list[:len(moves_list)] == moves_list:
                if len(opening.moves_list) > len(moves_list):
                    next_move = opening.moves_list[len(moves_list)]
                    next_moves[next_move] = next_moves.get(next_move, 0) + 1
      
        return sorted(next_moves, key=next_moves.get, reverse=True)

    def search_by_partial_moves(self, moves_sublist):
       
        results = []
        n = len(moves_sublist)
        for opening in self.openings.values():
            for i in range(len(opening.moves_list) - n + 1):
                if opening.moves_list[i:i+n] == moves_sublist:
                    results.append(opening)
                    break
        return results

    def __repr__(self):
        return f"<ChessOpeningsLibrary with {len(self.openings)} openings>"
