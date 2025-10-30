class Player:
    def __init__(self, name, balance, fish_caught, inventory):
        self.name = name
        self.balance = balance
        self.fish_caught = fish_caught
        self.inventory = inventory

class Settings:
    def __init__(self, fps, background):
        self.fps = fps
        self.background = background

class InvItem:
    def __init__(self, name, count):
        self.name = name
        self.count = count

class Button:
    def __init__(self, xpos, ypos, width, height, buttonText, onclickFunction):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.buttonText = buttonText
        self.onclickFunction = onclickFunction

        self.fillcolors = {
            'normal: FFED24',
            'hover: EBBE21,'
            'pressed: B39220'
        }

class gameFish:
    def __init__(self, species,color,attribute, dex_number):
        self.species = species
        self.color = color
        self.attribute = attribute
        self.dex_number = dex_number