from random import randint

from pygame import Surface
from pygame.image import load
from pygame.sprite import Sprite


class Player(Sprite):
    def __init__(self, image_path='./player_sprite.png', x=0, y=0):
        super().__init__()

        self.image = load(image_path)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = 7

        self.jumping = False
        self.falling = False

        self.jumping_count = 0

        self.jumping_height = 20
        self.jumping_speed = 20
        self.jumping_starting_pos_y = None

    def moveRight(self, player_ms):
        self.rect.x += player_ms

    def moveLeft(self, player_ms):
        self.rect.x -= player_ms

    def jump(self):
        self.jumping = True
        self.jumping_starting_pos_y = self.rect.y


class Opponent(Sprite):
    def __init__(self, image_path='./opponent_sprite.png', x=20, y=0, speed=7):
        super().__init__()

        self.image = load(image_path)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed

    def move(self):
        self.rect.x -= self.speed

        if self.rect.x <= 0:
            self.kill()


class Platform(Sprite):
    def __init__(self, x=0, y=0, resistance=0):
        super().__init__()

        self.image = Surface((randint(30, 200), randint(15, 30)))
        self.image.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y if y else randint(400, 600)
