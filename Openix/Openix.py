import chess
import re

class ChessOpening:
 

    def __init__(self, eco_code, name, moves_str):
        self.eco_code = eco_code
        self.name = name
        self.moves_str = moves_str
        self.moves_list = self.parse_moves(moves_str)

    def parse_moves(self, moves_str):
    
        cleaned = re.sub(r"\d+\.(\.\.)?", "", moves_str)
        cleaned = re.sub(r"[^\w\s+#=/-]", "", cleaned)
        tokens = cleaned.strip().split()
       
        return [tok for tok in tokens if re.match(r"^[a-hKQRNB][a-h1-8x\-O\-]*[+#=]?[\w]*$", tok)]

    def get_board_after_opening(self):
        board = chess.Board()
        for move_san in self.moves_list:
            try:
                move = board.parse_san(move_san)
                board.push(move)
            except Exception as e:
                print(f"Error applying move {move_san}: {e}")
                break
        return board

    @staticmethod
    def from_dict(data):
        eco_code = data.get("eco", "")
        name = data.get("name", "")
        moves_str = data.get("moves", "")
        return ChessOpening(eco_code, name, moves_str)

    @property
    def last_move(self):
  
        if self.moves_list:
            return self.moves_list[-1]
        return None

    @property
    def moves_count(self):
    
        return len(self.moves_list)

    def __repr__(self):
        return f"<Opening {self.eco_code} - {self.name}>"
