import pyglet
from Bubbles import Bubbles
import config as c

class BubbleGame:
    def __init__(self):
        self.score = 0
        self.score_label = pyglet.text.Label(text='Score: ' + str(self.score),
                                font_name='Arial',
                                font_size=18,
                                color = c.Game.SCORE_COLOR,
                                x=c.Window.WIDTH - 120, y= c.Window.HEIGHT - 30)

        Bubbles.create_bubbles()
        self.bubbles = Bubbles.bubbles


    def draw_game(self):
        Bubbles.draw_bubbles()
        self.score_label.draw()

    def update_game(self):
        Bubbles.update_bubbles()
        self.score = Bubbles.check_border(self.score)
        self.score_label.text = "Score: " + str(self.score)