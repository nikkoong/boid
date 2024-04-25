import pygame

class Reward:
    def __init__(self, x, y, radius) -> None:
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, (255,0,0), (int(self.x), int(self.y)), 10) #reward is a red circle
        pygame.draw.circle(screen, (255,0,0), (int(self.x), int(self.y)), self.radius, width=1)