class Game:

    ####### constructor #######
    def __init__(self, low = 0.4):

        self.low = low
        self.medium = 0.5
        self.high = 1.0 - low

        self.utility = ((self.low, self.low, self.low),
                        (self.medium, self.medium, 0.0),
                        (self.high, 0.0, 0.0))
