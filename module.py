class Module:
    def __init__(self, boards):
        self.RB = boards["RB"]
        self.PB = boards["PB"]
        self.is_m = True
        self.num = self.RB.num
        self.label = f"M{self.num}"

        self.PB_long = self.PB.total_long
        self.RB_long = self.RB.total_long
        self.RB_PB_short = self.RB.total_short + self.PB.total_short
        self.RB_short = self.RB.total_short

    def __add__(self, row):
        return row + self