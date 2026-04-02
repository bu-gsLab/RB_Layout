from yaml import safe_load
from module import Module

class Board:
    def __init__(self, type, num):
        self.type = type
        self.num = num
        self.label = type + str(num)

        self.is_rb = False
        self.is_pb = False

        if self.type == "RB":
            self.is_rb = True
        elif self.type == "PB":
            self.is_pb = True
        else:
            raise ValueError("Board type must be RB or PB")

        
        dims = self.load_dims()
        board_dims = dims[self.label]
        self.long = board_dims["long"]
        self.short = board_dims["short"]

        self.gap_top = board_dims["gap"]["top"]
        self.gap_bottom = board_dims["gap"]["bottom"]
        self.gap_left = board_dims["gap"]["left"]
        self.gap_right = board_dims["gap"]["right"]

        self.total_short = self.short + self.gap_top + self.gap_bottom
        self.total_long = self.long + self.gap_left + self.gap_right


    def __add__(self, b2):
        if self.is_rb and b2.is_pb:
            num = self.num
            boards = {"RB": self, "PB": b2}
        elif self.is_pb and b2.is_rb:
            num = b2.num
            boards = {"PB": self, "RB": b2}
        else:
            raise TypeError("Board addition only supported for RB + PB")
        
        return Module(boards)

    def load_dims(self):
        with open('dimensions.yaml', 'r') as f:
            data = safe_load(f)
        return data
