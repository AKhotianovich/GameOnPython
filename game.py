import json

import pgzrun
import shared
from coin import Coin
from constants import WIDTH, HEIGHT, TILE_SIZE
from enemy import Enemy
from hero import Hero
from shared import platforms

music.play("background_music")

background_image = "background"
finish_block = None
time = 0


def create_level():
    global finish_block, hero
    with open(f'lvls/lvl.json') as f:
        data = json.load(f)
    for lvl in data[f'level_{shared.level_now}']:
        shared.level_map.append(lvl)
        print(lvl)

    for y, row in enumerate(shared.level_map):
        for x, cell in enumerate(row):
            center_x = x * TILE_SIZE + TILE_SIZE // 2
            center_y = y * TILE_SIZE + TILE_SIZE // 2
            if cell == 'P':
                platform = Actor("platform", (center_x, center_y))
                platforms.append(platform)
            elif cell == 'F':
                finish_block = Actor("flag/0", (center_x, center_y))
            elif cell == 'C':
                coin = Coin('coin/0', (center_x, center_y))
                shared.coins.append(coin)

    for y, row in enumerate(shared.level_map):
        for x, cell in enumerate(row):
            center_x = x * TILE_SIZE + TILE_SIZE // 2
            center_y = y * TILE_SIZE + TILE_SIZE // 2
            if cell == 'E':
                enemy = Enemy((center_x, center_y))
                shared.enemies.append(enemy)

    hero = Hero((WIDTH // 2, HEIGHT - 100))


def draw():
    screen.clear()
    screen.blit(background_image, (0, 0))

    if not shared.game_started and not shared.game_over and not shared.game_win:
        draw_menu()
    else:
        hero.draw()
        for enemy in shared.enemies:
            enemy.draw()
        for platform in platforms:
            platform.draw()
        for coin in shared.coins:
            coin.draw()
        if finish_block:
            finish_block.draw()
        if shared.game_win:
            draw_game_win()
        if shared.game_over:
            draw_game_over()

        screen.draw.text(f"Coins: {len([coin for coin in shared.coins if coin.collected])}/{len(shared.coins)}",
                         topleft=(10, 10), fontsize=30, color="white")


def draw_menu():
    screen.draw.text("Mystic Explorer", center=(WIDTH // 2, HEIGHT // 2 - 100), fontsize=50, color="white")
    screen.draw.text("Press 'ENTER' to Start", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="white")
    screen.draw.text("Press 'S' to Toggle Sound", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30, color="white")
    screen.draw.text("Press 'Q' to Quit", center=(WIDTH // 2, HEIGHT // 2 + 100), fontsize=30, color="white")


def draw_game_over():
    screen.draw.text("Game Over!", center=(WIDTH // 2, HEIGHT // 2 - 100), fontsize=60, color="red")
    screen.draw.text("Press 'ENTER' to Restart", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="white")


def draw_game_win():
    screen.draw.text("You Win!", center=(WIDTH // 2, HEIGHT // 2 - 100), fontsize=60, color="green")
    screen.draw.text("Press 'ENTER' to Restart", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="white")


def update(dt):
    global finish_block, time, level_map
    if shared.game_started and not shared.game_over and not shared.game_win:
        hero.update()
        time += 0.03
        if time > 0.1:
            number = int(finish_block.image.split('/')[-1])
            finish_block.image = f'flag/{number + 1 % 49}'
        finish_block = Actor('flag/0', (finish_block.x, finish_block.y))
        for enemy in shared.enemies:
            enemy.update()
            if hero.actor.colliderect(enemy.actor):
                animate(hero.actor, y=HEIGHT + 8,
                        tween='bounce_start_end', duration=(HEIGHT - hero.actor.y) / 300)

                draw_game_over()
                shared.level_map = []
                music.play_once("game_over")
                shared.game_over = True
                shared.game_started = False

        for coin in shared.coins:
            if time > 0.1:
                number_coin = int(coin.actor.image.split('/')[-1])
                coin.actor.image = f'coin/{(number_coin + 1) % 6}'

            if coin.collect(hero):
                print("Монетка собрана!")

        if time > 0.1:
            time = 0

        if finish_block and hero.actor.colliderect(finish_block):
            animate(hero.actor, y=hero.actor.y - 60,
                    tween='bounce_start_end', duration=1)
            draw_game_win()
            music.play_once("win")
            shared.level_now += 1

            shared.game_win = True
            shared.game_started = False


def on_key_down(key):
    if key == keys.RETURN:
        shared.level_map.clear()
        shared.platforms.clear()
        shared.enemies.clear()
        shared.coins.clear()
        if not shared.game_started and not shared.game_over and not shared.game_win:
            shared.game_started = True
            shared.enemies.clear()
            create_level()
        elif shared.game_over or shared.game_win:
            shared.game_started = True
            shared.game_over = False
            shared.game_win = False
            music.play("background_music")
            shared.coins.clear()
            shared.enemies.clear()
            create_level()
    elif key == keys.S:
        shared.sound_enabled = not shared.sound_enabled
        if shared.sound_enabled:
            music.play("background_music")
        else:
            music.stop()
    elif key == keys.Q:
        exit()


pgzrun.go()
