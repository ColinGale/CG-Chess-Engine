import copy


class Move:
    def __init__(self, initial, final):
        # initial and final are square objects
        self.initial = initial
        self.final = final
        self.captured = None
        self.priority = 0
        self.notation = str(self.final.col_name) + str(8 - self.final.row)


    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final

    def __str__(self):
        return self.notation



