import random
from math import *
from ball import *
from constants import *

""" 
    The Main Class for managing the logic of the game plus with AI part to handle the computer pad, 
    main function is the main loop, it calls all the game logic. 
    update function : contains all the update() method of the game, same thing for draw().
"""


class Physics(object):
    def __init__(self):
        """Initalize the display and all game objects."""
        self.screen = pg.display.get_surface()
        self.Boundary = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = FPS_MAX
        self.keys = pg.key.get_pressed()
        self.done = False
        self.color = (255, 255, 255)  # game color
        self.player = Paddle(pg.Rect(10, 200, PAD_W, PAD_H), 0, PAD_SPEED, self.color)
        self.computer = Paddle(pg.Rect(870, 250, PAD_W, PAD_H), 0, PAD_SPEED + 1, self.color)
        self.ball = Ball(pg.Rect(400, 300, BL_DIM, BL_DIM), BL_XVEL, BL_YVEL, self.color)
        self.reactionAiDist = 100  # pixel
        self.errorInterval = 0
        self.predictionPoint = 0

    def update(self):
        # Update the player, computer, key pressed, ball, all stuffs & shits are updated here !
        self.keys = pg.key.get_pressed()
        self.player.update(self.Boundary)
        self.ball.update(self.Boundary, self.player.form, self.computer.form)
        # the AI fucntion.
        self.predict()

    def eventListener(self):
        # the event keys to interact with the player.
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.side = -1
                elif event.key == pg.K_DOWN:
                    self.player.side = 1
            else:
                self.player.side = 0

    def draw(self):
        # Draw all necessary objects to the level.
        self.screen.fill(BACHGROUND_COLOR)
        self.player.draw(self.screen)
        self.computer.draw(self.screen)
        self.ball.draw(self.screen)

    def mainLoop(self):
        # the main loop of the level.
        while not self.done:
            self.eventListener()
            self.update()
            self.draw()
            pg.display.flip()
            self.clock.tick(self.fps)

    """
        AI part functions:
    """

    def canPredict(self):
        return self.ball.xspeed > 0

    def canResponse(self, value):
        return self.ball.form.x > value

    def getNewDistReaction(self):
        if self.ball.form.colliderect(self.computer.form):
            # the distance reached by the ball to let ai react.
            self.reactionAiDist = random.randint(100, 400)
            self.errorInterval = random.randint(-30, 35)

    # predict the mouvement of the ball by the ia and move the center of paddle to it.
    def predict(self):

        # if the ball is attacking the ia, ia can predict.
        self.predictionPoint = self.computer.form.y + self.computer.form.h / 2

        if self.canPredict():

            self.getNewDistReaction()
            if self.predictionPoint > self.ball.form.y + self.errorInterval:
                self.computer.side = -1
            elif self.predictionPoint < self.ball.form.y + self.errorInterval:
                self.computer.side = 1
            # see if IA can response now or wait more
            if self.canResponse(self.reactionAiDist):
                self.computer.update(self.Boundary)
