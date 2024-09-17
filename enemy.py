from random import randint

import shared
from animated_sprite import AnimatedSprite
from shared import platforms


class Enemy(AnimatedSprite):
    def __init__(self, pos):
        super().__init__(["enemy_walk1", "enemy_walk2"], pos, randint(1, 5))
        self.direction = "left"
        self.platform_left = None
        self.platform_right = None
        self.spawn_platform = None
        self.find_spawn_platform()

    def find_spawn_platform(self):
        for block in shared.platforms:
            if (self.actor.x + self.actor.width - 1 > block.left and
                    self.actor.x - self.actor.width + 1 < block.right and
                    block.top + 10 >= self.actor.bottom >= block.top - 10):

                self.platform_left = block.left
                self.platform_right = block.right
                self.spawn_platform = block

                current_block = block
                while True:
                    next_block = next(
                        (b for b in shared.platforms if b.right == current_block.left + 2 and current_block.top == b.top),
                        None)
                    if next_block:
                        self.platform_left = next_block.left
                        current_block = next_block
                    else:
                        break

                current_block = block
                while True:
                    next_block = next(
                        (b for b in shared.platforms if b.left == current_block.right - 2 and current_block.top == b.top),
                        None)

                    if next_block:
                        self.platform_right = next_block.right
                        current_block = next_block
                    else:
                        break

                return

    def update(self):
        super().update()

        if self.is_on_platform() and shared.game_win is not True:
            if self.direction == "left":
                self.move("left")
                if self.actor.x <= self.platform_left:
                    self.direction = "right"
            else:
                self.move("right")
                if self.actor.x >= self.platform_right:
                    self.direction = "left"
        else:
            self.correct_position()

    def is_on_platform(self):
        if self.spawn_platform is not None and self.spawn_platform.top <= self.actor.bottom <= self.spawn_platform.top + 10:
            return True
        return False

    def collide_with_platform_edge(self, direction):
        if self.platform_left is not None and self.platform_right is not None:
            buffer = 5
            if direction == "left" and self.actor.left <= self.platform_left + buffer:
                return True
            elif direction == "right" and self.actor.right >= self.platform_right - buffer:
                return True
        return False

    def correct_position(self):
        if self.platform_left is not None and self.platform_right is not None:
            self.actor.y = self.spawn_platform.top - self.actor.height / 2
            if self.direction == "left":
                self.actor.x = max(self.actor.x, self.platform_left + 10)  # Запас от края платформы
            else:
                self.actor.x = min(self.actor.x, self.platform_right - 10)  # Запас от края платформы
