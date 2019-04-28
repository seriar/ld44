class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x = self.x + x
        self.y = self.y + y

    def neighbours(self):
        return [
            Cell(self.x - 1, self.y - 1),
            Cell(self.x - 1, self.y),
            Cell(self.x - 1, self.y + 1),
            Cell(self.x, self.y - 1),
            Cell(self.x, self.y + 1),
            Cell(self.x + 1, self.y - 1),
            Cell(self.x + 1, self.y),
            Cell(self.x + 1, self.y + 1),
        ]

    def __eq__(self, other):
        return hasattr(other, 'x') and hasattr(other, 'x') and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.to_str())

    def to_str(self):
        return str(self.x) + ':' + str(self.y)

    def is_in_box(self, min_x, min_y, max_x, max_y):
        return min_x <= self.x < max_x and min_y <= self.y < max_y
