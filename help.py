class HelpScreen:
    def __init__(self):
             ########################################
        self.message = [
            " Help ",
            "------",
            "",
            "Your goal is to terraform all the planet",
            "",
            "Your only resource is Cyber-Organic Nut-",
            "rient Woese Archaea - Y, or CONWA-Y or $",
            "",
            "You eat it, you plant it, you terraform ",
            "with it. You will die without it.",
            "",
            "You will win when all continents are te-",
            "rraformed or you have enough $ to do so.",
            "We think 10 mil $ should be enough.",
            "",
            "Good Luck, Operator!",
            "",
            "",
            "",
            "",
            "Operational Manual",
            "+--------------------------------------+",
            "|SPACE  |  PAUSE                       |",
            "|ESC    |  Back or Main menu           |",
            "|1 to 9 |  Select Continent            |",
            "|` or ~ |  Cancel Selection            |",
            "|return |  Confirm Selection           |",
            "|S      |  Sow Continent               |",
            "|H      |  Harvest Continent           |",
            "|T      |  Terraform Continent         |",
            "|arrows |  navigate                    |",
            "+--------------------------------------+"
        ]

    def get_size(self):
        max_x = 0
        for option in self.message:
            if len(option) > max_x:
                max_x = len(option)
        return max_x, len(self.message)
