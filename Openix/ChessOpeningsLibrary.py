import json
import os
import random
from Openix import ChessOpening

class ChessOpeningsLibrary:
    def __init__(self):
        self.openings = {}
        self._loaded_files = set()

    def load_from_json_file(self, file_path, raise_on_error=False):
        if file_path in self._loaded_files:
            return
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            if raise_on_error:
                raise
            else:
                print(f"Invalid JSON format in file: {file_path} - {e}")
                return
        loaded_count = 0
        if isinstance(data, dict):
            entries = data.values()
        elif isinstance(data, list):
            entries = data
        else:
            print(f"Unsupported JSON structure in file: {file_path}")
            return
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            try:
                opening = ChessOpening.from_dict(entry)
                if opening.eco_code and opening.moves_list:
                    eco = opening.eco_code
                    if eco not in self.openings:
                        self.openings[eco] = []
                    self.openings[eco].append(opening)
                    loaded_count += 1
            except Exception as e:
                print(f"Error loading opening: {entry.get('name', 'Unknown')} - {str(e)}")
                if raise_on_error:
                    raise
        self._loaded_files.add(file_path)

    def load_multiple_files(self, files_list, raise_on_error=False):
        for file_path in files_list:
            self.load_from_json_file(file_path, raise_on_error=raise_on_error)

    def find_by_eco(self, eco_code):
        return self.openings.get(eco_code, [])

    def search_by_name(self, name_substring):
        name_substring = name_substring.lower()
        results = []
        for openings in self.openings.values():
            for opening in openings:
                if name_substring in opening.name.lower():
                    results.append(opening)
        return results

    @staticmethod
    def _normalize_move(move):
        return move.lower().replace("+", "").replace("#", "").replace("=", "")

    def find_openings_starting_with(self, move_san):
        move_san_norm = self._normalize_move(move_san)
        results = []
        for openings in self.openings.values():
            for opening in openings:
                if opening.moves_list and self._normalize_move(opening.moves_list[0]) == move_san_norm:
                    results.append(opening)
        return results

    def find_openings_after_moves(self, moves_list):
        moves_norm = [self._normalize_move(m) for m in moves_list]
        results = []
        for openings in self.openings.values():
            for opening in openings:
                opening_moves_norm = [self._normalize_move(m) for m in opening.moves_list[:len(moves_norm)]]
                if opening_moves_norm == moves_norm:
                    results.append(opening)
        return results

    def get_random_opening(self):
        all_openings = self.get_all_openings()
        if not all_openings:
            return None
        return random.choice(all_openings)

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
        moves_norm = [self._normalize_move(m) for m in moves_list]
        next_moves = {}
        for openings in self.openings.values():
            for opening in openings:
                opening_moves_norm = [self._normalize_move(m) for m in opening.moves_list[:len(moves_norm)]]
                if opening_moves_norm == moves_norm:
                    if len(opening.moves_list) > len(moves_norm):
                        next_move = opening.moves_list[len(moves_norm)]
                        norm_next = self._normalize_move(next_move)
                        next_moves[norm_next] = next_moves.get(norm_next, 0) + 1
        return sorted(next_moves, key=next_moves.get, reverse=True)

    def search_by_partial_moves(self, moves_sublist):
        moves_norm = [self._normalize_move(m) for m in moves_sublist]
        n = len(moves_norm)
        results = []
        for openings in self.openings.values():
            for opening in openings:
                opening_moves_norm = [self._normalize_move(m) for m in opening.moves_list]
                for i in range(len(opening_moves_norm) - n + 1):
                    if opening_moves_norm[i:i+n] == moves_norm:
                        results.append(opening)
                        break
        return results

    def get_all_openings(self):
        all_openings = []
        for openings in self.openings.values():
            all_openings.extend(openings)
        return all_openings

    def get_statistics(self):
        stats = {
            'total_openings': len(self.get_all_openings()),
            'loaded_files': len(self._loaded_files),
            'moves_distribution': {}
        }
        for openings in self.openings.values():
            for opening in openings:
                first_move = opening.moves_list[0] if opening.moves_list else 'Unknown'
                norm_first = self._normalize_move(first_move)
                stats['moves_distribution'][norm_first] = stats['moves_distribution'].get(norm_first, 0) + 1
        return stats

    def __repr__(self):
        return f"<ChessOpeningsLibrary with {len(self.get_all_openings())} openings>"
