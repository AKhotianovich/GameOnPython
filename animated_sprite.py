from pgzero.actor import Actor


class AnimatedSprite:

    def __init__(self, images, pos, speed):
        self.images = images
        self.index = 0
        self.actor = Actor(self.images[self.index])
        self.actor.pos = pos
        self.speed = speed
        self.direction = "right"

    def draw(self):
        self.actor.draw()

    def update(self):
        self.index = (self.index + 0.2) % len(self.images)
        self.actor.image = self.images[int(self.index)]

    def move(self, direction):
        if direction == "left":
            self.actor.x -= self.speed
            self.direction = "left"
        elif direction == "right":
            self.actor.x += self.speed
            self.direction = "right"
