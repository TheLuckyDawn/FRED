from enum import Enum
class Position(Enum):
    NONE = "None"
    WR = "WR"
    RB = "RB"

    @staticmethod
    def from_str(label):
        if label.strip() in ('wr', 'WR'):
            return Position.WR
        elif label.strip() in ('rb', 'RB'):
            return Position.RB
        else:
            return Position.NONE

    def to_str(self):
        return self.value

class Roster:
    RB_LIMIT = 3
    WR_LIMIT = 3
    def __init__(self, name):
        self.name = name
        self.rbs = []
        self.wrs = []
        self.wins = 0
        self.losses = 0
        self.ties = 0

    def __contains__(self, player):
        if player in self.rbs or player in self.wrs:
            return True
        else:
            return False

    def __eq__(self, roster):
        if self.rbs == roster.rbs and self.wrs == roster.wrs:
            return True
        else:
            return False

    def win(self):
        self.wins += 1

    def lose(self):
        self.losses += 1

    def tie(self):
        self.ties += 1

    def printRecord(self):
        if self.ties == 0:
            print(f"{self.wins}-{self.losses}")
        else:
            print(f"{self.wins}-{self.losses}-{self.ties}")

    def addPlayer(self, player, position):
        if Position.WR == position:
            self.wrs.append(player)
        elif Position.RB == position:
            self.rbs.append(player)

    def getWRNumber(self):
        return len(self.wrs)

    def getRBNumber(self):
        return len(self.rbs)

    def full(self, position):
        if Position.WR == position:
            return Roster.getMaxPosition(Position.WR) - self.getWRNumber() <= 0
        elif Position.RB == position:
            return Roster.getMaxPosition(Position.RB) - self.getRBNumber() <= 0
        else:
            return True
    def getPosNumber(self, position):
        if Position.WR == position:
            return self.getWRNumber()
        elif Position.RB == position:
            return self.getRBNumber()
        else:
            return 0

    @staticmethod
    def getMaxPosition(position):
        if Position.WR == position:
            return Roster.WR_LIMIT
        elif Position.RB == position:
            return Roster.RB_LIMIT
        else:
            return 0

    def getPlayerList(self):
        return self.rbs + self.wrs

    def getRBs(self):
        return self.rbs

    def getWRs(self):
        return self.wrs

    def printRoster(self):
        print(f"--{self.name}'s Roster--")
        print("WRs:")
        for wr in self.wrs:
            print(wr)
        print("RBs:")
        for rb in self.rbs:
            print(rb)
        print("-----------------")