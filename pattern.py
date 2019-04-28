from cell import Cell


class Pattern:
    def __init__(self, cells):
        self.cells = cells

    def get_moved_cells(self, x, y):
        return [Cell(cell.x + x, cell.y + y) for cell in self.cells]


predefined = {
    'acorn': Pattern([
        Cell(0, 2),
        Cell(1, 2),
        Cell(1, 0),
        Cell(3, 1),
        Cell(4, 2),
        Cell(5, 2),
        Cell(6, 2)
    ]),
    'glider_gun': Pattern([
        Cell(0, 0),
        Cell(1, 0),
        Cell(2, 0),
        Cell(4, 0),
        Cell(0, 1),
        Cell(3, 2),
        Cell(4, 2),
        Cell(4, 3),
        Cell(4, 4),
        Cell(1, 3),
        Cell(2, 3),
        Cell(2, 4),
        Cell(0, 4),
    ])
}
