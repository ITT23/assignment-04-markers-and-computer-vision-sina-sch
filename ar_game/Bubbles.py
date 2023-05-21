import pyglet
import numpy as np
import random
import config as c
from typing import List, Any


def measure_distance(x1:int, y1:int, x2:int, y2:int) -> float:
    """measures the distance between two coordinates"""
    distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance

class Bubbles:
    bubbles = []
    def __init__(self, x = 200, y = c.Window.HEIGHT):
        self.x = x
        self.y = y
        # image source: https://de.cleanpng.com/png-rjxjvc/
        self.img = pyglet.resource.image("bubble.png")
        self.img.width = c.Bubble.WIDTH
        self.img.height = c.Bubble.HEIGHT
        self.bubble_spr = pyglet.sprite.Sprite(self.img, x=x, y=y)
        self.display = True
        
    def create_bubbles() -> None:
        """create random bubbles and save in a list"""
        for i in range(c.Bubble.NUM):
            Bubbles.bubbles.append(Bubbles(x = random.randint(0, c.Window.WIDTH - 1), y = c.Window.HEIGHT + i * 70))

    def draw_bubbles() -> None:
        """draw all bubbles"""
        for bubble in Bubbles.bubbles:
            if bubble.display:
                bubble.bubble_spr.draw()
    
    def update_bubbles() -> None:
        """update the posititon of all bubbles"""
        for bubble in Bubbles.bubbles:
            bubble.update_bubble()
  
    def update_bubble(self) -> None:
        """update the position of one bubble"""
        self.bubble_spr.y -= 1
    
    def collides_with(self, x:int, y:int) -> bool:
        """determine if a bubble collides with a finger/other object"""
        collision_distance = self.bubble_spr.width/2
        actual_distance = measure_distance(self.bubble_spr.x, self.bubble_spr.y, x, y)
        return (actual_distance <= collision_distance) and (self.bubble_spr.y >= y)

    def handle_collision_with(contours:List[Any]) -> None:
        """if a bubble collides with another object it disappears"""
        global score
        for bubble in Bubbles.bubbles:
            for contour in contours:
                x = contour[0][0][0]
                y = contour[0][0][1]
                # make sure bubbles don't disappear because of detection of the border
                if not x < 20 and not y < 20 and not x > c.Window.WIDTH - 20 and not y > c.Window.HEIGHT - 20:
                    if bubble.collides_with(x, y):
                        bubble.display = False
