class Piece:
    def __init__(self, column, row, shape, color):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = color
        self.rotation = 0