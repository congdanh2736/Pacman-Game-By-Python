from constants import *

class MazeBase(object):
    def __init__(self):
        self.portalPairs = {}
        self.homeoffset = (0, 0)
        self.ghostNodeDeny = {UP:(), DOWN:(), LEFT:(), RIGHT:()}

    def setPortalPairs(self, nodes):
        for pair in list(self.portalPairs.values()):
            nodes.setPortalPair(*pair)

    def connectHomeNodes(self, nodes):
        key = nodes.createHomeNodes(*self.homeoffset)
        nodes.connectHomeNodes(key, self.homenodeconnectLeft, LEFT)
        nodes.connectHomeNodes(key, self.homenodeconnectRight, RIGHT)

    def addOffset(self, x, y):
        return x + self.homeoffset[0], y + self.homeoffset[1]

    def denyGhostAccess(self, ghosts, nodes):
        nodes.denyAccessList(*(self.addOffset(2, 3) + (LEFT, ghosts)))
        nodes.denyAccessList(*(self.addOffset(2, 3) + (RIGHT, ghosts)))

        for direction in list(self.ghostNodeDeny.keys()):
            for values in self.ghostNodeDeny[direction]:
                nodes.denyAccessList(*(values) + (direction, ghosts))

class Maze1(MazeBase):
    def __init__(self):
        MazeBase.__init__(self)
        self.name = "maze1"
        self.portalPairs = {0:((0, 17), (27, 17))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (9, 14)
        self.homenodeconnectRight = (18, 14)
        self.pacmanStart = (15, 26)
        self.fruitStart = (9, 20)

        self.ghostNodeDeny = {
            UP:((9, 14), (18, 14), (11, 23), (16, 23)),
            LEFT:(self.addOffset(2, 3),),
            RIGHT:(self.addOffset(2, 3),)
        }

class Maze2(MazeBase):
    def __init__(self):
        MazeBase.__init__(self)
        self.name = "maze2"
        self.portalPairs = {0:((0, 4), (27, 4)), 1:((0, 26), (27, 26))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (9, 14)
        self.homenodeconnectRight = (18, 14)
        self.pacmanStart = (16, 26)
        self.fruitStart = (11, 20)
        self.ghostNodeDeny = {
            UP:((9, 14), (18, 14), (11, 23), (16, 23)),
            LEFT:(self.addOffset(2, 3),),
            RIGHT:(self.addOffset(2, 3),)
        }

class Maze3(MazeBase):
    def __init__(self):
        MazeBase.__init__(self)
        self.name = "maze3"
        self.portalPairs = {0:((0, 11), (27, 11)), 1:((0, 20), (27, 20))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (9, 14)
        self.homenodeconnectRight = (18, 14)
        self.pacmanStart = (15, 26)
        self.fruitStart = (12, 20)
        self.ghostNodeDeny = {
            UP:((9, 14), (18, 14), (11, 23), (16, 23)),
            LEFT:(self.addOffset(2, 3),),
            RIGHT:(self.addOffset(2, 3),)
        }

class Maze4(MazeBase):
    def __init__(self):
        MazeBase.__init__(self)
        self.name = "maze4"
        self.portalPairs = {0: ((0, 12), (27, 12))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (9, 14)
        self.homenodeconnectRight = (18, 14)
        self.pacmanStart = (15, 26)
        self.fruitStart = (12, 20)
        self.ghostNodeDeny = {
            UP: ((9, 14), (18, 14), (11, 23), (16, 23)),
            LEFT: (self.addOffset(2, 3),),
            RIGHT: (self.addOffset(2, 3),)
        }

class Maze5(MazeBase):
    def __init__(self):
        MazeBase.__init__(self)
        self.name = "maze5"
        self.portalPairs = {0: ((0, 16), (27, 16)), 1: ((0, 19), (27, 19))}
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (9, 14)
        self.homenodeconnectRight = (18, 14)
        self.pacmanStart = (15, 26)
        self.fruitStart = (12, 20)
        self.ghostNodeDeny = {
            UP: ((9, 14), (18, 14), (11, 23), (16, 23)),
            LEFT: (self.addOffset(2, 3),),
            RIGHT: (self.addOffset(2, 3),)
        }

class MazeData(object):
    def __init__(self):
        self.obj = None
        self.mazedict = {
            0:Maze1,
            1:Maze2,
            2:Maze3,
            3:Maze4,
            4:Maze5,
        }

    def loadMaze(self, level):
        self.obj = self.mazedict[level % len(self.mazedict)]()

