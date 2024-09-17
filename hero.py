from pgzero import music
from pgzero.builtins import Actor, keyboard, sounds

import shared

from animated_sprite import AnimatedSprite
from constants import WIDTH, HEIGHT
from shared import platforms


class Hero(AnimatedSprite):
    def __init__(self, pos):
        super().__init__(["hero_walk1", "hero_walk2"], pos, 3)
        self.health = 100
        self.jumping = False
        self.velocity_y = 0

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.velocity_y = -10
            sounds.jump.play()

    def update(self):
        super().update()

        self.actor.y += self.velocity_y
        self.velocity_y += 0.5

        platform_under = self.platform_under()
        if platform_under and self.velocity_y >= 0:
            self.jumping = False
            self.velocity_y = 0
            self.actor.y = platform_under.top - self.actor.height / 2

        if keyboard.left:
            self.move("left")
            if self.collide_with_platforms("left"):
                self.move("right")
        if keyboard.right:
            self.move("right")
            if self.collide_with_platforms("right"):
                self.move("left")
        if keyboard.up and not self.jumping:
            self.jump()

        if self.actor.left < 0:
            self.actor.left = 0
        elif self.actor.right > WIDTH:
            self.actor.right = WIDTH

        if self.actor.top > HEIGHT:
            shared.level_map = []
            shared.game_over = True
            shared.game_started = False
            music.play_once("game_over")

    def platform_under(self):
        for block in platforms:
            if (self.actor.x + self.actor.width // 2 > block.left and
                    self.actor.x - self.actor.width // 2 < block.right and
                    block.top + 10 >= self.actor.bottom >= block.top - 10 and
                    self.velocity_y >= 0):
                return block
        return None

    def collide_with_platforms(self, direction):
        for block in platforms:
            if self.actor.colliderect(block):
                if direction == "left" and self.actor.left < block.right < self.actor.right:
                    return True
                elif direction == "right" and self.actor.right > block.left > self.actor.left:
                    return True
        return False
