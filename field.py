from cell import Cell

HARVEST_RATE = 3


class Field:
    def __init__(self, id, w, h, price):
        self.id = id
        self.width = int(w)
        self.height = int(h)
        self.cells = []
        self.prev_cells = []
        self.is_locked = True
        self.income = 0
        self.age = 0
        self.total = 0
        self.spent = 0
        self.price = price
        self.sowing = []
        self.sowing_price = 0
        self.is_sowing = False
        self.cursor = Cell(0, 0)

    def add_cell(self, cell):
        self.cells.append(cell)

    def add_cells(self, cells):
        for cell in cells:
            self.cells.append(cell)

    def start_sowing(self):
        self.is_sowing = True

    def sow(self):
        self.cells = self.sowing
        self.sowing = []
        self.sowing_price = 0
        self.cursor = Cell(0, 0)
        self.is_sowing = False

    def cancel_sowing(self):
        self.sowing = []
        self.sowing_price = 0
        self.cursor = Cell(0, 0)
        self.is_sowing = False

    def add_sowing_cell(self, cell):
        if cell in self.sowing:
            self.sowing.remove(cell)
        else:
            self.sowing.append(Cell(cell.x, cell.y))
        self.sowing_price = int(len(self.sowing) * len(self.sowing) / 2)

    def unlock(self):
        self.is_locked = False

    def get_data(self):
        return self.cells, self.x, self.y

    def move_cursor(self, x, y):
        self.cursor.move(x, y)

    def step(self, steps=1):
        gross_income = 0
        for step in range(steps):
            self.age = self.age + 1
            self.evolve()
            gross_income = gross_income + self.trim()
        self.total += gross_income
        return gross_income

    def trim(self):
        trimmed = []
        for cell in self.cells:
            if cell.is_in_box(0, 0, self.width, self.height):
                trimmed.append(cell)
        income = len(self.cells) - len(trimmed)
        self.cells = trimmed
        self.income = income
        return income

    def harvest(self):
        collected = int(len(self.cells) / HARVEST_RATE)
        self.total += collected
        self.cells = []
        self.income = 0
        self.prev_cells = []
        return collected

    def is_big(self):
        return self.width > 39 or self.height > 39

    def get_status(self):
        if self.is_locked:
            return ["",
                    "",
                    "LOCKED",
                    "Size:" + str(self.width) + "x" + str(self.height),
                    "$:" + str(self.price)
                    ]
        return [
            "Size:" + str(self.width) + "x" + str(self.height),
            "Inc:" + str(self.income),
            "Age:" + str(self.age),
            "Cls:" + str(len(self.cells)),
            "TOT:" + str(self.total),
            "COST:" + str(self.spent),
        ]

    def evolve(self):
        """
        Evolves the list of cells using Conway's GoL rules

        """
        # list of candidates which may stay alive / be born
        candidates = {}
        # list of cells in the next stage
        new_cells = []
        self.prev_cells = self.cells
        for cell in self.cells:
            # count occurrence of cells as neighbours of old cells
            for n in cell.neighbours():
                if n in candidates:
                    candidates[n] = candidates[n] + 1
                else:
                    candidates[n] = 1
            # check candidates:
        for c in candidates:
            # existing cells with 2 neighbours will stay alive
            if candidates[c] == 2 and c in self.prev_cells:
                # logging.info("Adding cell: %s" % c.to_str())
                new_cells.append(c)
            # any cell with 3 neighbours will be alive next turn
            elif candidates[c] == 3:
                # logging.info("Adding cell: %s" % c.to_str())
                new_cells.append(c)

        self.cells = new_cells

    def render(self, renderer, screen):
        scr_w, scr_h = screen.get_size()
        field_rendered_width = self.width * renderer.tile_size
        field_rendered_height = self.height * renderer.tile_size
        offset_x = (scr_w - field_rendered_width) / 2
        offset_y = (scr_h - field_rendered_height) / 2
        screen.fill((0, 0, 0))

        screen_border = screen.subsurface(offset_x - renderer.tile_size,
                                          offset_y - renderer.tile_size,
                                          field_rendered_width + 2 * renderer.tile_size,
                                          field_rendered_height + 2 * renderer.tile_size)
        screen_border.fill((0, 127, 255))

        screen_field = screen_border.subsurface(renderer.tile_size,
                                                renderer.tile_size,
                                                field_rendered_width,
                                                field_rendered_height)
        if self.is_locked:
            renderer.render_line(screen_field, "locked", 2, 2)
        else:
            if self.is_sowing:
                renderer.render_template_cells(screen_field, self.sowing, self.cursor)
            else:
                renderer.render_cells(screen_field, self.cells)
