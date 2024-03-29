import pygame as pg
from settings import *
vec = pg.math.Vector2


def add_walls(game, tiles):
    for tile in tiles:
        Wall(game, tile[0], tile[1])


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.dir = 0
        self.is_move = False
        self.last_move = 0

    def move(self, dx=0, dy=0):
        now = pg.time.get_ticks()
        if now - self.last_move > PLAYER_MOVE_DELAY:
            can_move = True
            for wall in self.game.walls:
                if not (wall.pos.x != self.pos.x + dx or wall.pos.y != self.pos.y + dy):
                    can_move = False
            if can_move:
                self.last_move = now
                self.pos.x += dx
                self.pos.y += dy
                self.rect.x = self.pos.x * TILESIZE
                self.rect.y = self.pos.y * TILESIZE

    def update(self):
        wall_left, wall_front, wall_right = False, False, False
        if self.game.lines[int(vec(1, 0).rotate(-90 + self.dir).y + self.pos.y)][
                           int(vec(1, 0).rotate(-90 + self.dir).x + self.pos.x)] == '#':
            wall_left = True
        if self.game.lines[int(vec(1, 0).rotate(self.dir).y + self.pos.y)][
                           int(vec(1, 0).rotate(self.dir).x + self.pos.x)] == '#':
            wall_front = True
        if self.game.lines[int(vec(1, 0).rotate(90 + self.dir).y + self.pos.y)][
                           int(vec(1, 0).rotate(90 + self.dir).x + self.pos.x)] == '#':
            wall_right = True

        now = pg.time.get_ticks()
        if now - self.last_move > PLAYER_MOVE_DELAY:
            # print((wall_left, wall_front, wall_right))
            if not wall_left:
                self.dir -= 90
                self.pos += vec(1, 0).rotate(self.dir)
                self.game.path_string += '-90f;'
            elif not wall_front:
                self.pos += vec(1, 0).rotate(self.dir)
                self.game.path_string += 'f;'
            elif not wall_right:
                self.dir += 90
                self.pos += vec(1, 0).rotate(self.dir)
                self.game.path_string += '90f;'
            elif wall_left and wall_front and wall_right:
                self.dir += 180
                self.game.path_tiles[int(self.pos.y)][int(self.pos.x)] = False
                self.pos += vec(1, 0).rotate(self.dir)
                self.game.path_string += '180f;'

            if -1 < self.game.loops_count[int(self.pos.y)][int(self.pos.x)] <= 1:
                # ways = 0
                # if self.game.lines[int(self.pos.y) - 1][int(self.pos.x)] != '#':
                #     ways += 1
                # if self.game.lines[int(self.pos.y) + 1][int(self.pos.x)] != '#':
                #     ways += 1
                # if self.game.lines[int(self.pos.y)][int(self.pos.x) - 1] != '#':
                #     ways += 1
                # if self.game.lines[int(self.pos.y)][int(self.pos.x) + 1] != '#':
                #     ways += 1
                self.game.loops_count[int(self.pos.y)][int(self.pos.x) + 1] = -1
                self.game.path_tiles[int(self.pos.y)][int(self.pos.x)] = False
            elif self.game.loops_count[int(self.pos.y)][int(self.pos.x)] > -1:
                self.game.path_tiles[int(self.pos.y)][int(self.pos.x)] = True
                self.game.loops_count[int(self.pos.y)][int(self.pos.x)] -= 1

            # self.game.path_tiles[int(self.pos.y)][int(self.pos.x)] = not self.game.path_tiles[int(self.pos.y)][int(self.pos.x)]
            # print(self.dir)
            self.last_move = now
            self.rect.x = self.pos.x * TILESIZE
            self.rect.y = self.pos.y * TILESIZE
            # Path(self.game, self.pos.x, self.pos.y)


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Exit(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Path(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.paths
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
