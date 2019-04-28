from cell import Cell


class Field:
    def __init__(self, id, w, h):
        self.id = id
        self.width = w
        self.height = h
        self.cells = []
        self.prev_cells = []
        self.is_running = False
        self.is_locked = True
        self.income = 0
        self.age = 0

    def add_cell(self, cell):
        self.cells.append(cell)

    def add_cells(self, cells):
        for cell in cells:
            self.cells.append(cell)

    def unlock(self):
        self.is_locked = False

    def start(self):
        self.is_running = True

    def stop(self):
        self.is_running = False

    def get_data(self):
        return self.cells, self.x, self.y

    def step(self, steps=1):
        gross_income = 0
        if self.is_running:
            for step in range(steps):
                self.age = self.age + 1
                self.evolve()
                gross_income = gross_income + self.trim()
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

    def get_status(self):
        if self.is_locked:
            return ["",
                    "",
                    "",
                    "LOCKED"]
        return [
            "Active" if self.is_running else "Inactive",
            "Inc:" + str(self.income),
            "Age:" + str(self.age),
            "Cls:" + str(len(self.cells))
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
            renderer.render_cells(screen_field, self.cells)
