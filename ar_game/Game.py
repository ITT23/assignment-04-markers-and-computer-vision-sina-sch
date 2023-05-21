import pyglet
from Bubbles import Bubbles
import config as c

class BubbleGame:
    def __init__(self):
        self.score = 0
        self.score_label = pyglet.text.Label(text='Score: ' + str(self.score),
                                font_name='Arial',
                                font_size=18,
                                color = c.Game.TEXT_COLOR,
                                x=c.Window.WIDTH - 120, y= c.Window.HEIGHT - 30)
        self.is_over = False
        self.game_over_label = pyglet.text.Label("The game is over. To restart, press 'r'. To quit, press 'q'.",
                                                font_name='Arial',
                                                font_size=20,
                                                color = c.Game.TEXT_COLOR,
                                                x=c.Window.WIDTH / 2,
                                                y=c.Window.HEIGHT - c.Window.HEIGHT/3,
                                                anchor_x='center',
                                                anchor_y='center')
        Bubbles.create_bubbles()


    def draw_game(self) -> None:
        """draw bubbles and score label"""
        if not self.is_over:
            Bubbles.draw_bubbles()
            self.score_label.draw()
        else:
            self.game_over_label.draw()

    def update_game(self) -> None:
        """update position of bubbles and the current score"""
        Bubbles.update_bubbles()
        self.score = Bubbles.check_border(self.score)
        self.score_label.text = "Score: " + str(self.score)
        self.over()

    def over(self) -> None:
        """determine if the game is over"""
        self.is_over = not Bubbles.bubbles[0].display 
        for bubble in Bubbles.bubbles:
            self.is_over = not bubble.display and self.is_over

    def restart(self) -> None:
        """restart the game"""
        self.is_over = False
        self.score = 0
        Bubbles.create_bubbles()