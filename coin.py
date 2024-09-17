from pgzero.actor import Actor
from pgzero.loaders import sounds


class Coin:
    def __init__(self, image, pos):
        self.actor = Actor(image, pos)
        self.collected = False

    def draw(self):
        if not self.collected:
            self.actor.draw()

    def collect(self, hero):
        if not self.collected and self.actor.colliderect(hero.actor):
            self.collected = True
            sounds.coin.play()
            return True
        return False
