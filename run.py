import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pauser import Pause
from text import TextGroup, Text
from sprites import LifeSprites
from sprites import MazeSprites
from mazedata import MazeData

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None

        self.background_norm = None
        self.background_flash = None

        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0

        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)

        self.fruitCaptured = []

        self.mazedata = MazeData()

        self.selected_index = 0
        self.menu_positions = [280, 310, 340]

        self.selected_index_Acvm = 0
        self.menu_positions_Acvm = [175, 265]

        self.player_name = ""
        self.score = 0
        self.input_active = False
        self.input_text = ""

        self.achievementScreen = False

    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)

        self.fruitCaptured = []

        self.selected_index = 0
        # self.arrow = Text("→", YELLOW, 80, self.menu_positions[self.selected_index], 16)

        self.loadTitleScreen()

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)

    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.textgroup.updateLevel(self.level)

    def setBackground(self):

        # self.background = pygame.surface.Surface(SCREENSIZE).convert()
        # self.background.fill(BLACK)

        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        self.background_norm = self.mazesprites.constructBackground(self.background_norm, self.level % 5)
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)
        self.flashBG = False
        self.background = self.background_norm

    def startGame(self):
        pygame.mixer.music.stop()
        self.small_pellet_sound = pygame.mixer.Sound("assets/sounds/pacman_chomp.wav")
        self.eat_ghost_sound = pygame.mixer.Sound("assets/sounds/pacman_eatghost.wav")
        self.eat_fruit_sound = pygame.mixer.Sound("assets/sounds/pacman_eatfruit.wav")
        self.freight_mode_sound = pygame.mixer.Sound("assets/sounds/pacman_intermission.wav")
        self.begin_sound = pygame.mixer.Sound("assets/sounds/pacman_beginning.wav")
        self.death_sound = pygame.mixer.Sound("assets/sounds/pacman_death.wav")
        self.channel0 = pygame.mixer.Channel(0)

        self.mazedata.loadMaze(self.level)
        self.mazesprites = MazeSprites("assets/maze/"+self.mazedata.obj.name+".txt", "assets/maze/"+self.mazedata.obj.name+"_rotation.txt")
        self.setBackground()
        self.nodes = NodeGroup("assets/maze/"+self.mazedata.obj.name+".txt")
        self.mazedata.obj.setPortalPairs(self.nodes)
        self.mazedata.obj.connectHomeNodes(self.nodes)

        self.pacman = Pacman(self.nodes.getNodeFromTiles(*self.mazedata.obj.pacmanStart))
        self.pellets = PelletGroup("assets/maze/"+self.mazedata.obj.name+".txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)

        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 0)))
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(0, 3)))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(4, 3)))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))

        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)

        self.mazedata.obj.denyGhostAccess(self.ghosts, self.nodes)

        self.ghosts.blinky.sprites.setLevel(self.level)
        self.ghosts.pinky.sprites.setLevel(self.level)
        self.ghosts.inky.sprites.setLevel(self.level)
        self.ghosts.clyde.sprites.setLevel(self.level)

        self.title_screen = False
        # self.mazesprites = MazeSprites("maze1.txt", "maze1_rotation.txt")
        # self.background = self.mazesprites.constructBackground(self.background, self.level % 5)

        # self.nodes = NodeGroup("maze1.txt")
        # self.nodes.setPortalPair((0,17), (27,17))
        # homekey = self.nodes.createHomeNodes(11.5, 14)
        # self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        # self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)
        # self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26))
        # self.pellets = PelletGroup("maze1.txt")
        # self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 0+14))
        # self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        # self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(0+11.5, 3+14))
        # self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(4+11.5, 3+14))
        # self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        # self.nodes.denyAccessList(2+11.5, 3+14, LEFT, self.ghosts)
        # self.nodes.denyAccessList(2+11.5, 3+14, RIGHT, self.ghosts)
        # self.nodes.denyAccessList(12, 14, UP, self.ghosts)
        # self.nodes.denyAccessList(15, 14, UP, self.ghosts)
        # self.nodes.denyAccessList(12, 26, UP, self.ghosts)
        # self.nodes.denyAccessList(15, 26, UP, self.ghosts)

    def update(self):
        dt = self.clock.tick(240) / 1000.0
        if not self.title_screen:
            self.textgroup.update(dt)
            self.pellets.update(dt)
            if not self.pause.paused:
                # self.pacman.update(dt)
                self.ghosts.update(dt)
                if self.fruit is not None:
                    self.fruit.update(dt)
                self.checkPelletEvents()
                self.checkGhostEvents()
                self.checkFruitEvents()

            if self.pacman.alive:
                if not self.pause.paused:
                    self.pacman.update(dt)
            else:
                self.pacman.update(dt)

            if self.flashBG:
                self.flashTimer += dt
                if self.flashTimer >= self.flashTime:
                    self.flashTimer = 0
                    if self.background == self.background_norm:
                        self.background = self.background_flash
                    else:
                        self.background = self.background_norm

            afterPauseMethod = self.pause.update(dt)
            if afterPauseMethod is not None:
                afterPauseMethod()
        else:
            pass
        self.checkEvents()
        self.render()

    def checkBegin(self):
        self.playBeginSound()

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.playEatGhostSound()
                    self.pacman.visible = False
                    ghost.visible = False
                    self.updateScore(ghost.points)
                    self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()
                    self.nodes.allowHomeAccess(ghost)
                elif ghost.mode.current is not SPAWN:
                     if self.pacman.alive:
                         self.lives -=  1
                         self.lifesprites.removeImage()
                         self.pacman.die()
                         self.ghosts.hide()
                         self.playDeathSound()
                         pygame.mixer.music.stop()
                         if self.lives <= 0:
                             self.textgroup.showText(GAMEOVERTXT)
                             self.pause.setPause(pauseTime=3, func=self.restartGame)
                             with open("assets/scores.txt", "a", encoding="utf-8") as f:
                                 f.write(f"{self.player_name}: {self.score}\n")
                         else:
                             self.pause.setPause(pauseTime=3, func=self.resetLevel)

    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(*self.mazedata.obj.fruitStart), self.level)
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.playEatFruitSound()
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
                fruitCaptured = False

                for fruit in self.fruitCaptured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruitCaptured = True
                        break;
                if not fruitCaptured:
                    self.fruitCaptured.append(self.fruit.image)

                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.playSmallPelletSound()
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                self.playFreightModeSound()
                self.ghosts.startFreight()
            if self.pellets.isEmpty():
                self.flashBG = True
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)

    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    def render(self):
        self.screen.blit(self.background, (0, 0))

        if not self.title_screen:
            # self.nodes.render(self.screen)
            self.pellets.render(self.screen)
            if self.fruit is not None:
                self.fruit.render(self.screen)
            self.pacman.render(self.screen)
            self.ghosts.render(self.screen)
            self.textgroup.render(self.screen)

            for i in range(len(self.lifesprites.images)):
                x = self.lifesprites.images[i].get_width() * i
                y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
                self.screen.blit(self.lifesprites.images[i], (x, y))

            for i in range(len(self.fruitCaptured)):
                x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i + 1)
                y = SCREENHEIGHT - self.fruitCaptured[i].get_height()

                self.screen.blit(self.fruitCaptured[i], (x, y))
        else:
            self.titleText.render(self.screen)
            self.startText.render(self.screen)
            self.achievementText.render(self.screen)
            self.exitText.render(self.screen)
            self.arrow.render(self.screen)

            if self.input_active:
                self.screen.fill(BLACK)
                # prompt = self.titleText.font.render("Enter your name: \n" + self.input_text, True, WHITE)
                # self.screen.blit(prompt, (100, 200))

                self.inputnameText = Text("Enter your name:", YELLOW, 32, 100 ,16)
                self.inputname = Text(self.input_text, WHITE, 32, 140 ,16)
                self.inputnameText.render(self.screen)
                self.inputname.render(self.screen)
                pygame.display.update()
                return

            if self.achievementScreen:
                self.screen.fill(BLACK)

                with open("assets/scores.txt", "r") as f:
                    # textScore = f.read()
                    y_line = 50
                    i = 1
                    for textScore in f:
                        self.scoreText = Text("TOP 5 ON SCORE BOARD", YELLOW, 33, 10, 20)
                        self.scoreText.render(self.screen)

                        textScore.strip()
                        textScore.replace("\n", "")
                        self.scoreBoard = Text(f"{i}. {textScore}", WHITE, 0, y_line, 16)
                        self.scoreBoard.render(self.screen)
                        y_line += 20
                        i += 1
                        if i == 6:
                            break;

                # self.loadChoosenAchievementScreen(self)
                self.exitAcvmText.render(self.screen)
                self.startAcvmText.render(self.screen)

                self.arrowAchieve.render(self.screen)

        pygame.display.update()

    def loadTitleScreen(self):
        self.title_screen = True
        self.setTitleScreenBackground()
        self.titleText = Text("PACMAN", YELLOW, 32, 40, 64)
        self.startText = Text("START GAME", YELLOW, 120, 280, 16)
        self.achievementText = Text("SCORE BOARD", WHITE, 120, 310, 16)
        self.exitText = Text("EXIT", WHITE, 120, 340, 16)
        pygame.mixer.music.load("assets/sounds/pacman_beginning.wav")
        pygame.mixer.music.play(loops=-1)

    def loadChoosenScreen(self):
        self.arrow = Text("→", YELLOW, 80, self.menu_positions[self.selected_index], 16)

    def loadChoosenAchievementScreen(self):
        self.exitAcvmText = Text("exit", YELLOW, 150, SCREENHEIGHT - 16, 16)
        self.startAcvmText = Text("play", WHITE, 240, SCREENHEIGHT - 16, 16)

        self.arrowAchieve = Text("↓", YELLOW, 175, SCREENHEIGHT - 40, 16)
        # self.arrowAchieve = Text("↓", YELLOW, 265, SCREENHEIGHT - 40, 16)

    def setTitleScreenBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def playSmallPelletSound(self):
        if not self.channel0.get_busy():
            self.channel0.play(self.small_pellet_sound)

    def playEatGhostSound(self):
        pygame.mixer.find_channel(True).play(self.eat_ghost_sound)

    def playEatFruitSound(self):
        pygame.mixer.find_channel(True).play(self.eat_fruit_sound)

    def playFreightModeSound(self):
        pygame.mixer.find_channel(True).play(self.freight_mode_sound, -1, 7000)

    def stopFreightModeSound(self):
        self.freight_mode_sound.stop()

    def playBeginSound(self):
        self.channel0.play(self.begin_sound)

    def playDeathSound(self):
        pygame.mixer.find_channel(True).play(self.death_sound)

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if self.input_active:
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.player_name = self.input_text
                        self.input_active = False
                        self.startGame()
                    elif event.key == K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode

            elif self.achievementScreen:
                if event.type == KEYDOWN:
                    if event.key == K_LEFT or event.key == K_a:

                        pygame.mixer.music.load("assets/sounds/button_click.ogg")
                        pygame.mixer.music.play()

                        self.selected_index_Acvm = (self.selected_index_Acvm - 1) % len(self.menu_positions_Acvm)
                        if self.selected_index_Acvm == 0:
                            self.arrowAchieve = Text("↓", YELLOW, self.menu_positions_Acvm[self.selected_index_Acvm], SCREENHEIGHT - 40, 16)
                            self.exitAcvmText = Text("exit", YELLOW, 150, SCREENHEIGHT - 16, 16)
                            self.startAcvmText = Text("play", WHITE, 240, SCREENHEIGHT - 16, 16)
                        if self.selected_index_Acvm == 1:
                            self.arrowAchieve = Text("↓", YELLOW, self.menu_positions_Acvm[self.selected_index_Acvm], SCREENHEIGHT - 40, 16)
                            self.exitAcvmText = Text("exit", WHITE, 150, SCREENHEIGHT - 16, 16)
                            self.startAcvmText = Text("play", YELLOW, 240, SCREENHEIGHT - 16, 16)
                    elif event.key == K_RIGHT or event.key == K_d:

                        pygame.mixer.music.load("assets/sounds/button_click.ogg")
                        pygame.mixer.music.play()

                        self.selected_index_Acvm = (self.selected_index_Acvm + 1) % len(self.menu_positions_Acvm)
                        if self.selected_index_Acvm == 0:
                            self.arrowAchieve = Text("↓", YELLOW, self.menu_positions_Acvm[self.selected_index_Acvm], SCREENHEIGHT - 40, 16)
                            self.exitAcvmText = Text("exit", YELLOW, 150, SCREENHEIGHT - 16, 16)
                            self.startAcvmText = Text("play", WHITE, 240, SCREENHEIGHT - 16, 16)
                        if self.selected_index_Acvm == 1:
                            self.arrowAchieve = Text("↓", YELLOW, self.menu_positions_Acvm[self.selected_index_Acvm], SCREENHEIGHT - 40, 16)
                            self.exitAcvmText = Text("exit", WHITE, 150, SCREENHEIGHT - 16, 16)
                            self.startAcvmText = Text("play", YELLOW, 240, SCREENHEIGHT - 16, 16)
                    # if event.key == K_BACKSPACE:
                    #     self.achievementScreen = False
                    elif event.key == K_RETURN:
                        if self.selected_index_Acvm == 0:
                            self.achievementScreen = False
                        elif self.selected_index_Acvm == 1:
                            self.input_active = True
                            self.achievementScreen = False

            elif event.type == KEYDOWN:
                if not self.title_screen:
                    if event.key == K_SPACE:
                        if self.pacman.alive:
                            self.pause.setPause(playerPaused=True)
                            if not self.pause.paused:
                                self.textgroup.hideText()
                                self.showEntities()
                            else:
                                self.textgroup.showText(PAUSETXT)
                                self.hideEntities()
                else:

                    if event.key == K_DOWN or event.key == K_s:

                        pygame.mixer.music.load("assets/sounds/button_click.ogg")
                        pygame.mixer.music.play()

                        self.selected_index = (self.selected_index + 1) % len(self.menu_positions)
                        self.arrow = Text("→", YELLOW, 80, self.menu_positions[self.selected_index], 16)
                        if self.selected_index == 0:
                            self.startText = Text("START GAME", YELLOW, 120, 280, 16)
                            self.achievementText = Text("SCORE BOARD", WHITE, 120, 310, 16)
                            self.exitText = Text("EXIT", WHITE, 120, 340, 16)
                        elif self.selected_index == 1:
                            self.startText = Text("START GAME", WHITE, 120, 280, 16)
                            self.achievementText = Text("SCORE BOARD", YELLOW, 120, 310, 16)
                            self.exitText = Text("EXIT", WHITE, 120, 340, 16)
                        elif self.selected_index == 2:
                            self.startText = Text("START GAME", WHITE, 120, 280, 16)
                            self.achievementText = Text("SCORE BOARD", WHITE, 120, 310, 16)
                            self.exitText = Text("EXIT", YELLOW, 120, 340, 16)
                    elif event.key == K_UP or event.key == K_w:

                        pygame.mixer.music.load("assets/sounds/button_click.ogg")
                        pygame.mixer.music.play()

                        self.selected_index = (self.selected_index - 1) % len(self.menu_positions)
                        self.arrow = Text("→", YELLOW, 80, self.menu_positions[self.selected_index], 16)
                        if self.selected_index == 0:
                            self.startText = Text("START GAME", YELLOW, 120, 280, 16)
                            self.achievementText = Text("SCORE BOARD", WHITE, 120, 310, 16)
                            self.exitText = Text("EXIT", WHITE, 120, 340, 16)
                        elif self.selected_index == 1:
                            self.startText = Text("START GAME", WHITE, 120, 280, 16)
                            self.achievementText = Text("SCORE BOARD", YELLOW, 120, 310, 16)
                            self.exitText = Text("EXIT", WHITE, 120, 340, 16)
                        elif self.selected_index == 2:
                            self.startText = Text("START GAME", WHITE, 120, 280, 16)
                            self.achievementText = Text("SCORE BOARD", WHITE, 120, 310, 16)
                            self.exitText = Text("EXIT", YELLOW, 120, 340, 16)
                    elif event.key == K_RETURN:
                        if self.selected_index == 0:
                            # self.startGame()

                            self.input_active = True
                            self.input_text = ""

                        elif self.selected_index == 1:
                            self.achievementScreen = True
                        elif self.selected_index == 2:
                            exit()


if __name__ == "__main__":
    game = GameController()
    # game.startGame()

    game.loadTitleScreen()
    game.loadChoosenScreen()
    game.loadChoosenAchievementScreen()

    pygame.display.set_caption("Pacman")
    icon = pygame.image.load("assets/image/icon.png")
    pygame.display.set_icon(icon)

    while True:
        game.update()