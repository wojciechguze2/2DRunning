import os
import sys
from random import randint

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

SPRITE_SIZE = 100

GROUND_Y = WINDOW_HEIGHT - WINDOW_PADDING * 4 - SPRITE_SIZE

player_sprite = sprites.Player(
    x=WINDOW_PADDING * 2,
    y=GROUND_Y
)

player_group = pygame.sprite.Group(player_sprite)
opponents_group = pygame.sprite.Group()
platforms_group = pygame.sprite.Group()

pygame.display.update()

main_loop_counter = 0
opponent = None
hit_times = 0


def update_pygame_display(fps=75):
    pygame.display.flip()
    fps_clock.tick(fps)


def update_sprite_groups():
    player_group.update()
    player_group.draw(screen)

    opponents_group.update()
    opponents_group.draw(screen)

    platforms_group.update()
    platforms_group.draw(screen)


def get_rect_pos(rect) -> dict:
    return {
        'left_bottom': (rect.x, rect.y + rect.height),  # todo: change tuple to dict
        'right_bottom': (rect.x + rect.width, rect.y + rect.height),
        'left_top': (rect.x, rect.y),
        'right_top': (rect.x + rect.width, rect.y),
        'y': rect.y,
        'x': rect.x
    }


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
            and player_sprite.rect.top > WINDOW_PADDING and not (player_sprite.jumping or player_sprite.falling):
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
        player_sprite.falling = True
        player_sprite.jumping = False
        player_sprite.jumping_count = 0
        # print('end jumping / start falling')

    if player_sprite.falling and player_sprite.jumping_starting_pos_y is not None \
            and player_rect.y < player_sprite.jumping_starting_pos_y:
        player_rect.y += player_sprite.jumping_speed
        # print('falling')

    if player_sprite.falling and player_sprite.jumping_starting_pos_y and \
            player_rect.y >= player_sprite.jumping_starting_pos_y:
        player_sprite.rect.y = player_sprite.jumping_starting_pos_y
        player_sprite.falling = False
        player_sprite.jumping_starting_pos_y = None
        # print('end falling %d' % player_rect.y)

    player_pos = get_rect_pos(player_rect)

    platforms_poses = []

    for platform in platforms_group:
        if platform.rect.x <= 0:
            platform.kill()

        platforms_poses.append(get_rect_pos(platform.rect))

    player_collides_platform = False

    for platform_pose in platforms_poses:
        player_collides_platform_y = abs(player_rect.y + player_rect.height - platform_pose['y']) < 10

        platform_top_surface_x = range(platform_pose['left_top'][0], platform_pose['right_top'][0])
        player_collides_platform_x = list(
                set(
                    range(player_pos['left_bottom'][0], player_pos['right_bottom'][0])
                ).intersection(platform_top_surface_x)
        )

        player_collides_platform = bool(player_collides_platform_x) and player_collides_platform_y

    if player_collides_platform and player_sprite.falling:
        player_sprite.falling = False
        player_sprite.jumping = False
        player_sprite.jumping_starting_pos_y = None
    elif not player_collides_platform and player_rect.y < GROUND_Y \
            and not (player_sprite.jumping or player_sprite.falling):
        player_rect.y += player_sprite.jumping_speed / 4

    if not opponents_group.sprites():
        if main_loop_counter / 100 - hit_times > 7:
            opponent_speed = main_loop_counter / 100 - hit_times
        else:
            opponent_speed = 7

        print('Opponent speed: %.2f' % opponent_speed)

        opponent = sprites.Opponent(
            x=WINDOW_WIDTH,
            y=GROUND_Y,
            speed=opponent_speed
        )

        opponents_group.add(opponent)

    if opponent:
        opponent.move()

    if randint(0, 150) == 3 and platforms_group.__len__() < 1:
        platforms_group.add(sprites.Platform(x=WINDOW_WIDTH))

    for platform in platforms_group.sprites():
        platform.rect.x -= 4

    if player_rect.colliderect(opponent.rect):
        hit_times += 1
        print('You got hit %d times' % hit_times)
        opponent.kill()

    update_sprite_groups()
    update_pygame_display()
