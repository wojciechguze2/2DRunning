import os
import sys

import pygame
from pygame.locals import *

import sprites

pygame.init()

# fonts
monospace_12 = pygame.font.SysFont('monospace', 12)

# window settings
WINDOW_POSITION_X = 100
WINDOW_POSITION_Y = 100

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_PADDING = 20

os.environ['SDL_VIDEO_WINDOW_POS'] = '%s, %s' % (WINDOW_POSITION_X, WINDOW_POSITION_Y)

fps_clock = pygame.time.Clock()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('2d running')

PLAYER_SPRITE_SIZE = 100

player_sprite = sprites.Player(
    x=WINDOW_PADDING * 2,
    y=WINDOW_HEIGHT - WINDOW_PADDING * 2 - PLAYER_SPRITE_SIZE
)

player_group = pygame.sprite.Group(player_sprite)
# opponents_group = pygame.sprite.Group()

pygame.display.update()

main_loop_counter = 0


def update_pygame_display(fps=75):
    pygame.display.flip()
    fps_clock.tick(fps)


def update_sprite_groups():
    player_group.update()
    player_group.draw(screen)

    """
    opponents_group.update()
    opponents_group.draw(screen)
    """


while True:
    main_loop_counter += 1
    key_pressed = pygame.key.get_pressed()

    player_rect = player_group.sprites()[0].rect

    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            # .rect.collidepoint(mouse_pos)

    if key_pressed[pygame.K_ESCAPE]:
        break

    if (key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]) \
            and player_sprite.rect.left > WINDOW_PADDING:
        player_sprite.moveLeft(player_sprite.speed)

    if (key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]) \
            and player_sprite.rect.right < (WINDOW_WIDTH - WINDOW_PADDING):
        player_sprite.moveRight(player_sprite.speed)

    if (key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]) \
            and player_sprite.rect.top > WINDOW_PADDING and not (player_sprite.jumping or player_sprite.failing):
        player_sprite.jump()

    if player_sprite.jumping and player_sprite.jumping_count < player_sprite.jumping_height / 2:
        player_rect.y -= player_sprite.jumping_speed
        player_sprite.jumping_count += 1
        # print('jumping 1 stage')
    elif player_sprite.jumping and player_sprite.jumping_count >= player_sprite.jumping_height / 2:
        player_rect.y -= player_sprite.jumping_speed / 3
        player_sprite.jumping_count += 1
        # print('jumping 2 stage')

    if player_sprite.jumping and player_sprite.jumping_count >= player_sprite.jumping_height:
        player_sprite.failing = True
        player_sprite.jumping = False
        player_sprite.jumping_count = 0
        # print('end jumping / start failing')

    if player_sprite.failing and player_sprite.jumping_starting_pos_y is not None \
            and player_rect.y < player_sprite.jumping_starting_pos_y:
        player_rect.y += player_sprite.jumping_speed
        # print('failing')

    if player_sprite.failing and player_rect.y >= player_sprite.jumping_starting_pos_y:
        player_sprite.rect.y = player_sprite.jumping_starting_pos_y
        player_sprite.failing = False
        player_sprite.jumping_starting_pos_y = None
        # print('end failing %d' % player_rect.y)

    if key_pressed[pygame.K_SPACE] and player_sprite.rect.left:
        facing = -1
    elif key_pressed[pygame.K_SPACE] and not player_sprite.rect.left:
        facing = 1

    update_sprite_groups()
    update_pygame_display()
