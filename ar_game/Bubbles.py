import pyglet
import numpy as np
from typing import List, Any

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480


xs = [200, 300, 220, 110, 50, 170, 280, 330, 400, 470]

def measure_distance(x1:int, y1:int, x2:int, y2:int) -> float:
    """measures the distance between two coordinates"""
    distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance

class Bubbles:
    bubbles = []
    def __init__(self, x = 200, y = WINDOW_HEIGHT):
        self.x = x
        self.y = y
        # image source: https://de.cleanpng.com/png-rjxjvc/
        self.img = pyglet.resource.image("bubble.png")
        self.img.width = 50
        self.img.height = 50
        self.bubble_spr = pyglet.sprite.Sprite(self.img, x=x, y=y)
        self.display = True
        
    def create_bubbles() -> None:
        """create random bubbles and save in a list"""
        for i in range(10):
            Bubbles.bubbles.append(Bubbles(x = xs[i], y = WINDOW_HEIGHT + i * 70))

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
                if not x < 20 and not y < 20 and not x > 620 and not y > 340:
                    if bubble.collides_with(x, y):
                        bubble.display = False
