import logging

logging.basicConfig(
    filename='log/ld44.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-6s %(message)s'
)


class Menu:
    def __init__(self):
        self.selected = 0
        self.options = [
            "CONTINUE",
            "RESTART",
            "HELP",
            "ABOUT",
            "EXIT"
        ]

    def select(self, i):
        if 0 <= i < len(self.options):
            self.selected = i
        elif i >= len(self.options):
            self.select(i - len(self.options))
        elif i < 0:
            self.select(i + len(self.options))

    def get_options_with_selection(self):
        options = []
        for i, option in enumerate(self.options):
            if i == self.selected:
                options.append("> " + option)
            else:
                options.append("  " + option)
        return options

    def get_size_with_selection(self):
        max_x = 0
        for option in self.options:
            if len(option) + 2 > max_x:
                max_x = len(option) + 2
        return max_x, len(self.options)

    def get_size(self):
        max_x = 0
        for option in self.options:
            if len(option) > max_x:
                max_x = len(option)
        return max_x, len(self.options)

    def next(self):
        self.select(self.selected + 1)
        logging.info(self.selected)

    def prev(self):
        self.select(self.selected - 1)
        logging.info(self.selected)

    def act(self):
        logging.info("Acting on selected: %d - %s" % (self.selected, self.options[self.selected]))
        if self.selected == 0:
            return 'cont'
        if self.selected == 1:
            return 'new'
        if self.selected == 2:
            return 'help'
        elif self.selected == 3:
            return 'about'
        elif self.selected == 4:
            return 'exit'
