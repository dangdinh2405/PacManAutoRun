# Build Pac-Man from Scratch in Python with PyGame!!
import copy

import ChooseMode
from matrix import matrix
import pygame
import math

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id, powerup, eaten_ghost, screen,
                 spooked_img, dead_img, HEIGHT, WIDTH, level):
        self.level = level
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.dead_img = dead_img
        self.spooked_img = spooked_img
        self.screen = screen
        self.eaten_ghost = eaten_ghost
        self.powerup = powerup
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not self.powerup and not self.dead) or (self.eaten_ghost[self.id] and self.powerup and not self.dead):
            self.screen.blit(self.img, (self.x_pos, self.y_pos))
        elif self.powerup and not self.dead and not self.eaten_ghost[self.id]:
            self.screen.blit(self.spooked_img, (self.x_pos, self.y_pos))
        else:
            self.screen.blit(self.dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        # R, L, U, D
        num1 = ((self.HEIGHT - 50) // 32)
        num2 = (self.WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if self.level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if self.level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (self.level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if self.level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (self.level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if self.level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (self.level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if self.level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (self.level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if self.level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (self.level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if self.level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (self.level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if self.level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (self.level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if self.level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (self.level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if self.level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (self.level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if self.level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (self.level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if self.level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (self.level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if self.level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (self.level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_clyde(self):
        # r, l, u, d
        # clyde is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_blinky(self):
        # r, l, u, d
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_inky(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_pinky(self):
        # r, l, u, d
        # inky is going to turn left or right whenever advantageous, but only up or down on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction


class PacmanGame:
    def __init__(self):

        pygame.init()
        self.WIDTH = 900
        self.HEIGHT = 950
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.level = copy.deepcopy(matrix)
        self.color = 'blue'
        self.PI = math.pi
        self.player_images = [pygame.transform.scale(pygame.image.load(f'pacman_image/{i}.png'), (45, 45)) for i
                              in range(1, 5)]
        self.blinky_img = pygame.transform.scale(pygame.image.load(f'ghost_images/red.png'), (45, 45))
        self.pinky_img = pygame.transform.scale(pygame.image.load(f'ghost_images/pink.png'), (45, 45))
        self.inky_img = pygame.transform.scale(pygame.image.load(f'ghost_images/blue.png'), (45, 45))
        self.clyde_img = pygame.transform.scale(pygame.image.load(f'ghost_images/orange.png'), (45, 45))
        self.spooked_img = pygame.transform.scale(pygame.image.load(f'ghost_images/powerup.png'), (45, 45))
        self.dead_img = pygame.transform.scale(pygame.image.load(f'ghost_images/dead.png'), (45, 45))

        self.paused = False

        self.center_x = 0
        self.center_y = 0

        self.player_x = 450
        self.player_y = 663
        self.direction = 0
        self.blinky_x = 56
        self.blinky_y = 58
        self.blinky_direction = 0
        self.inky_x = 440
        self.inky_y = 388
        self.inky_direction = 2
        self.pinky_x = 440
        self.pinky_y = 438
        self.pinky_direction = 2
        self.clyde_x = 440
        self.clyde_y = 438
        self.clyde_direction = 2
        self.counter = 0
        self.flicker = False
        self.turns_allowed = [False, False, False, False]
        self.direction_command = 0
        self.player_speed = 2
        self.score = 0
        self.powerup = False
        self.power_counter = 0
        self.eaten_ghost = [False, False, False, False]
        self.targets = [(self.player_x, self.player_y)] * 4
        self.blinky_dead = False
        self.inky_dead = False
        self.clyde_dead = False
        self.pinky_dead = False
        self.blinky_box = False
        self.inky_box = False
        self.clyde_box = False
        self.pinky_box = False
        self.moving = False
        self.ghost_speeds = [2, 2, 2, 2]
        self.startup_counter = 0
        self.lives = 3
        self.game_over = False
        self.game_won = False


    def draw_misc(self):
        score_text = self.font.render(f'Score: {self.score}', True, 'white')
        self.screen.blit(score_text, (10, 920))
        if self.powerup:
            pygame.draw.circle(self.screen, 'blue', (140, 930), 15)
        for i in range(self.lives):
            self.screen.blit(pygame.transform.scale(self.player_images[0], (30, 30)), (650 + i * 40, 915))
        if self.game_over:
            pygame.draw.rect(self.screen, 'white', [50, 200, 800, 300],0, 10)
            pygame.draw.rect(self.screen, 'dark gray', [70, 220, 760, 260], 0, 10)
            gameover_text = self.font.render('Game over! Space bar to restart!', True, 'red')
            self.screen.blit(gameover_text, (100, 300))
        if self.game_won:
            pygame.draw.rect(self.screen, 'white', [50, 200, 800, 300],0, 10)
            pygame.draw.rect(self.screen, 'dark gray', [70, 220, 760, 260], 0, 10)
            gameover_text = self.font.render('Victory! Space bar to restart!', True, 'green')
            self.screen.blit(gameover_text, (100, 300))


    def check_collisions(self, scor, power, power_count, eaten_ghosts):
        num1 = (self.HEIGHT - 50) // 32
        num2 = self.WIDTH // 30
        if 0 < self.player_x < 870:
            if self.level[self.center_y // num1][self.center_x // num2] == 1:
                self.level[self.center_y // num1][self.center_x // num2] = 0
                scor += 10
            if self.level[self.center_y // num1][self.center_x // num2] == 2:
                self.level[self.center_y // num1][self.center_x // num2] = 0
                scor += 50
                power = True
                power_count = 0
                eaten_ghosts = [False, False, False, False]
        return scor, power, power_count, eaten_ghosts

    def draw_board(self):
        num1 = ((self.HEIGHT - 50) // 32)
        num2 = (self.WIDTH // 30)
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if self.level[i][j] == 1:
                    pygame.draw.circle(self.screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
                if self.level[i][j] == 2 and not self.flicker:
                    pygame.draw.circle(self.screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
                if self.level[i][j] == 3:
                    pygame.draw.line(self.screen, self.color, (j * num2 + (0.5 * num2), i * num1),
                                     (j * num2 + (0.5 * num2), i * num1 + num1), 3)
                if self.level[i][j] == 4:
                    pygame.draw.line(self.screen, self.color, (j * num2, i * num1 + (0.5 * num1)),
                                     (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
                if self.level[i][j] == 5:
                    pygame.draw.arc(self.screen, self.color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                    0, self.PI / 2, 3)
                if self.level[i][j] == 6:
                    pygame.draw.arc(self.screen, self.color,
                                    [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], self.PI / 2, self.PI, 3)
                if self.level[i][j] == 7:
                    pygame.draw.arc(self.screen, self.color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], self.PI,
                                    3 * self.PI / 2, 3)
                if self.level[i][j] == 8:
                    pygame.draw.arc(self.screen, self.color,
                                    [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * self.PI / 2,
                                    2 * self.PI, 3)
                if self.level[i][j] == 9:
                    pygame.draw.line(self.screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                     (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


    def draw_player(self):
        # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
        if self.direction == 0:
            self.screen.blit(self.player_images[self.counter // 5], (self.player_x, self.player_y))
        elif self.direction == 1:
            self.screen.blit(pygame.transform.flip(self.player_images[self.counter // 5], True, False), (self.player_x, self.player_y))
        elif self.direction == 2:
            self.screen.blit(pygame.transform.rotate(self.player_images[self.counter // 5], 90), (self.player_x, self.player_y))
        elif self.direction == 3:
            self.screen.blit(pygame.transform.rotate(self.player_images[self.counter // 5], 270), (self.player_x, self.player_y))


    def check_position(self, centerx, centery):
        turns = [False, False, False, False]
        num1 = (self.HEIGHT - 50) // 32
        num2 = (self.WIDTH // 30)
        num3 = 15
        # check collisions based on center x and center y of player +/- fudge number
        if centerx // 30 < 29:
            if self.direction == 0:
                if self.level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
            if self.direction == 1:
                if self.level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
            if self.direction == 2:
                if self.level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
            if self.direction == 3:
                if self.level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= centerx % num2 <= 18:
                    if self.level[(centery + num3) // num1][centerx // num2] < 3:
                        turns[3] = True
                    if self.level[(centery - num3) // num1][centerx // num2] < 3:
                        turns[2] = True
                if 12 <= centery % num1 <= 18:
                    if self.level[centery // num1][(centerx - num2) // num2] < 3:
                        turns[1] = True
                    if self.level[centery // num1][(centerx + num2) // num2] < 3:
                        turns[0] = True
            if self.direction == 0 or self.direction == 1:
                if 12 <= centerx % num2 <= 18:
                    if self.level[(centery + num1) // num1][centerx // num2] < 3:
                        turns[3] = True
                    if self.level[(centery - num1) // num1][centerx // num2] < 3:
                        turns[2] = True
                if 12 <= centery % num1 <= 18:
                    if self.level[centery // num1][(centerx - num3) // num2] < 3:
                        turns[1] = True
                    if self.level[centery // num1][(centerx + num3) // num2] < 3:
                        turns[0] = True
        else:
            turns[0] = True
            turns[1] = True

        return turns

    def move_player(self, play_x, play_y):
        # r, l, u, d
        if self.direction == 0 and self.turns_allowed[0]:
            play_x += self.player_speed
        elif self.direction == 1 and self.turns_allowed[1]:
            play_x -= self.player_speed
        if self.direction == 2 and self.turns_allowed[2]:
            play_y -= self.player_speed
        elif self.direction == 3 and self.turns_allowed[3]:
            play_y += self.player_speed
        return play_x, play_y

    def get_targets(self, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, blinky, inky, pinky, clyde):
        if self.player_x < 450:
            runaway_x = 900
        else:
            runaway_x = 0
        if self.player_y < 450:
            runaway_y = 900
        else:
            runaway_y = 0
        return_target = (380, 400)
        if self.powerup:
            if not blinky.dead and not self.eaten_ghost[0]:
                blink_target = (runaway_x, runaway_y)
            elif not blinky.dead and self.eaten_ghost[0]:
                if 340 < blink_x < 560 and 340 < blink_y < 500:
                    blink_target = (400, 100)
                else:
                    blink_target = (self.player_x,self.player_y)
            else:
                blink_target = return_target
            if not inky.dead and not self.eaten_ghost[1]:
                ink_target = (runaway_x, self.player_y)
            elif not inky.dead and self.eaten_ghost[1]:
                if 340 < ink_x < 560 and 340 < ink_y < 500:
                    ink_target = (400, 100)
                else:
                    ink_target = (self.player_x, self.player_y)
            else:
                ink_target = return_target
            if not pinky.dead:
                pink_target = (self.player_x, runaway_y)
            elif not pinky.dead and self.eaten_ghost[2]:
                if 340 < pink_x < 560 and 340 < pink_y < 500:
                    pink_target = (400, 100)
                else:
                    pink_target = (self.player_x, self.player_y)
            else:
                pink_target = return_target
            if not pinky.dead and not self.eaten_ghost[3]:
                clyd_target = (450, 450)
            elif not clyde.dead and self.eaten_ghost[3]:
                if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                    clyd_target = (400, 100)
                else:
                    clyd_target = (self.player_x, self.player_y)
            else:
                clyd_target = return_target
        else:
            if not blinky.dead:
                if 340 < blink_x < 560 and 340 < blink_y < 500:
                    blink_target = (400, 100)
                else:
                    blink_target = (self.player_x, self.player_y)
            else:
                blink_target = return_target
            if not inky.dead:
                if 340 < ink_x < 560 and 340 < ink_y < 500:
                    ink_target = (400, 100)
                else:
                    ink_target = (self.player_x, self.player_y)
            else:
                ink_target = return_target
            if not pinky.dead:
                if 340 < pink_x < 560 and 340 < pink_y < 500:
                    pink_target = (400, 100)
                else:
                    pink_target = (self.player_x, self.player_y)
            else:
                pink_target = return_target
            if not clyde.dead:
                if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                    clyd_target = (400, 100)
                else:
                    clyd_target = (self.player_x, self.player_y)
            else:
                clyd_target = return_target
        return [blink_target, ink_target, pink_target, clyd_target]

    def toggle_pause(self):
        self.paused = not self.paused

    def run_game(self):
        global inky, pinky, blinky, clyde
        run = True
        while run:
            if not self.paused:
                if self.counter < 19:
                    self.counter += 1
                    if self.counter > 3:
                        self.flicker = False
                else:
                    self.counter = 0
                    self.flicker = True
                if self.powerup and self.power_counter < 600:
                    self.power_counter += 1
                elif self.powerup and self.power_counter >= 600:
                    self.power_counter = 0
                    self.powerup = False
                    self.eaten_ghost = [False, False, False, False]
                if self.startup_counter < 180 and not self.game_over and not self.game_won:
                    self.moving = False
                    self.startup_counter += 1
                else:
                    self.moving = True

                if self.moving:
                    self.player_x, self.player_y = self.move_player(self.player_x, self.player_y)
                    if not self.blinky_dead and not blinky.in_box:
                        self.blinky_x, self.blinky_y, self.blinky_direction = blinky.move_blinky()
                    else:
                        self.blinky_x, self.blinky_y, self.blinky_direction = blinky.move_clyde()
                    if not self.pinky_dead and not pinky.in_box:
                        self.pinky_x, self.pinky_y, self.pinky_direction = pinky.move_pinky()
                    else:
                        self.pinky_x, self.pinky_y, self.pinky_direction = pinky.move_clyde()
                    if not self.inky_dead and not inky.in_box:
                        self.inky_x, self.inky_y, self.inky_direction = inky.move_inky()
                    else:
                        self.inky_x, self.inky_y, self.inky_direction = inky.move_clyde()
                    self.clyde_x, self.clyde_y, self.clyde_direction = clyde.move_clyde()

            self.timer.tick(self.fps)
            self.screen.fill('black')
            self.draw_board()
            self.center_x = self.player_x + 23
            self.center_y = self.player_y + 24
            if self.powerup:
                self.ghost_speeds = [1, 1, 1, 1]
            else:
                self.ghost_speeds = [2, 2, 2, 2]
            if self.eaten_ghost[0]:
                self.ghost_speeds[0] = 2
            if self.eaten_ghost[1]:
                self.ghost_speeds[1] = 2
            if self.eaten_ghost[2]:
                self.ghost_speeds[2] = 2
            if self.eaten_ghost[3]:
                self.ghost_speeds[3] = 2
            if self.blinky_dead:
                self.ghost_speeds[0] = 4
            if self.inky_dead:
                self.ghost_speeds[1] = 4
            if self.pinky_dead:
                self.ghost_speeds[2] = 4
            if self.clyde_dead:
                self.ghost_speeds[3] = 4

            self.game_won = True
            for i in range(len(self.level)):
                if 1 in self.level[i] or 2 in self.level[i]:
                    self.game_won = False

            player_circle = pygame.draw.circle(self.screen, 'black', (self.center_x, self.center_y), 20, 2)
            self.draw_player()
            blinky = Ghost(self.blinky_x, self.blinky_y, self.targets[0], self.ghost_speeds[0], self.blinky_img,
                           self.blinky_direction, self.blinky_dead, self.blinky_box, 0, self.powerup, self.eaten_ghost, self.screen, self.spooked_img, self.dead_img, self.HEIGHT, self.WIDTH, self.level)
            inky = Ghost(self.inky_x, self.inky_y, self.targets[1], self.ghost_speeds[1], self.inky_img,
                         self.inky_direction, self.inky_dead, self.inky_box, 1, self.powerup, self.eaten_ghost, self.screen, self.spooked_img, self.dead_img, self.HEIGHT, self.WIDTH, self.level)
            pinky = Ghost(self.pinky_x, self.pinky_y, self.targets[2], self.ghost_speeds[2], self.pinky_img,
                          self.pinky_direction, self.pinky_dead, self.pinky_box, 2, self.powerup, self.eaten_ghost, self.screen, self.spooked_img, self.dead_img, self.HEIGHT, self.WIDTH, self.level)
            clyde = Ghost(self.clyde_x, self.clyde_y, self.targets[3], self.ghost_speeds[3], self.clyde_img,
                          self.clyde_direction, self.clyde_dead, self.clyde_box, 3, self.powerup, self.eaten_ghost, self.screen, self.spooked_img, self.dead_img, self.HEIGHT, self.WIDTH, self.level)
            self.draw_misc()
            self.targets = self.get_targets(self.blinky_x, self.blinky_y, self.inky_x, self.inky_y, self.pinky_x, self.pinky_y, self.clyde_x, self.clyde_y, blinky, inky, pinky, clyde)

            self.turns_allowed = self.check_position(self.center_x, self.center_y)
            self.score, self.powerup, self.power_counter, self.eaten_ghost = self.check_collisions(self.score, self.powerup, self.power_counter, self.eaten_ghost)
            if not self.powerup:
                if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
                        (player_circle.colliderect(inky.rect) and not inky.dead) or \
                        (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
                        (player_circle.colliderect(clyde.rect) and not clyde.dead):
                    if self.lives > 0:
                        self.lives -= 1
                        self.startup_counter = 0
                        self.powerup = False
                        self.power_counter = 0
                        self.player_x = 450
                        self.player_y = 663
                        self.direction = 0
                        self.direction_command = 0
                        self.blinky_x = 56
                        self.blinky_y = 58
                        self.blinky_direction = 0
                        self.inky_x = 440
                        self.inky_y = 388
                        self.inky_direction = 2
                        self.pinky_x = 440
                        self.pinky_y = 438
                        self.pinky_direction = 2
                        self.clyde_x = 440
                        self.clyde_y = 438
                        self.clyde_direction = 2
                        self.eaten_ghost = [False, False, False, False]
                        self.blinky_dead = False
                        self.inky_dead = False
                        self.clyde_dead = False
                        self.pinky_dead = False
                    else:
                        self.game_over = True
                        self.moving = False
                        self.startup_counter = 0
            if self.powerup and player_circle.colliderect(blinky.rect) and self.eaten_ghost[0] and not blinky.dead:
                if self.lives > 0:
                    self.powerup = False
                    self.power_counter = 0
                    self.lives -= 1
                    self.startup_counter = 0
                    self.player_x = 450
                    self.player_y = 663
                    self.direction = 0
                    self.direction_command = 0
                    self.blinky_x = 56
                    self.blinky_y = 58
                    self.blinky_direction = 0
                    self.inky_x = 440
                    self.inky_y = 388
                    self.inky_direction = 2
                    self.pinky_x = 440
                    self.pinky_y = 438
                    self. pinky_direction = 2
                    self.clyde_x = 440
                    self.clyde_y = 438
                    self.clyde_direction = 2
                    self.eaten_ghost = [False, False, False, False]
                    self.blinky_dead = False
                    self.inky_dead = False
                    self.clyde_dead = False
                    self.pinky_dead = False
                else:
                    self.game_over = True
                    self.moving = False
                    self.startup_counter = 0
            if self.powerup and player_circle.colliderect(inky.rect) and self.eaten_ghost[1] and not inky.dead:
                if self.lives > 0:
                    self.powerup = False
                    self.power_counter = 0
                    self.lives -= 1
                    self.startup_counter = 0
                    self.player_x = 450
                    self.player_y = 663
                    self.direction = 0
                    self.direction_command = 0
                    self.blinky_x = 56
                    self.blinky_y = 58
                    self.blinky_direction = 0
                    self.inky_x = 440
                    self.inky_y = 388
                    self.inky_direction = 2
                    self.pinky_x = 440
                    self.pinky_y = 438
                    self.pinky_direction = 2
                    self.clyde_x = 440
                    self.clyde_y = 438
                    self.clyde_direction = 2
                    self.eaten_ghost = [False, False, False, False]
                    self.blinky_dead = False
                    self.inky_dead = False
                    self.clyde_dead = False
                    self.pinky_dead = False
                else:
                    self.game_over = True
                    self.moving = False
                    self.startup_counter = 0
            if self.powerup and player_circle.colliderect(pinky.rect) and self.eaten_ghost[2] and not pinky.dead:
                if self.lives > 0:
                    self.powerup = False
                    self.power_counter = 0
                    self.lives -= 1
                    self.startup_counter = 0
                    self.player_x = 450
                    self.player_y = 663
                    self.direction = 0
                    self.direction_command = 0
                    self.blinky_x = 56
                    self.blinky_y = 58
                    self.blinky_direction = 0
                    self.inky_x = 440
                    self.inky_y = 388
                    self.inky_direction = 2
                    self.pinky_x = 440
                    self.pinky_y = 438
                    self.pinky_direction = 2
                    self.clyde_x = 440
                    self.clyde_y = 438
                    self.clyde_direction = 2
                    self.eaten_ghost = [False, False, False, False]
                    self.blinky_dead = False
                    self.inky_dead = False
                    self.clyde_dead = False
                    self.pinky_dead = False
                else:
                    self.game_over = True
                    self.moving = False
                    self.startup_counter = 0
            if self.powerup and player_circle.colliderect(clyde.rect) and self.eaten_ghost[3] and not clyde.dead:
                if self.lives > 0:
                    self.powerup = False
                    self.power_counter = 0
                    self.lives -= 1
                    self.startup_counter = 0
                    self.player_x = 450
                    self.player_y = 663
                    self.direction = 0
                    self.direction_command = 0
                    self.blinky_x = 56
                    self.blinky_y = 58
                    self.blinky_direction = 0
                    self.inky_x = 440
                    self.inky_y = 388
                    self.inky_direction = 2
                    self.pinky_x = 440
                    self.pinky_y = 438
                    self.pinky_direction = 2
                    self.clyde_x = 440
                    self.clyde_y = 438
                    self.clyde_direction = 2
                    self.eaten_ghost = [False, False, False, False]
                    self.blinky_dead = False
                    self.inky_dead = False
                    self.clyde_dead = False
                    self.pinky_dead = False
                else:
                    self.game_over = True
                    self.moving = False
                    self.startup_counter = 0
            if self.powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not self.eaten_ghost[0]:
                self.blinky_dead = True
                self.eaten_ghost[0] = True
                self.score += (2 ** self.eaten_ghost.count(True)) * 100
            if self.powerup and player_circle.colliderect(inky.rect) and not inky.dead and not self.eaten_ghost[1]:
                self.inky_dead = True
                self.eaten_ghost[1] = True
                self.score += (2 ** self.eaten_ghost.count(True)) * 100
            if self.powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not self.eaten_ghost[2]:
                self.pinky_dead = True
                self.eaten_ghost[2] = True
                self.score += (2 ** self.eaten_ghost.count(True)) * 100
            if self.powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not self.eaten_ghost[3]:
                self.clyde_dead = True
                self.eaten_ghost[3] = True
                self.score += (2 ** self.eaten_ghost.count(True)) * 100

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.direction_command = 0
                    if event.key == pygame.K_LEFT:
                        self.direction_command = 1
                    if event.key == pygame.K_UP:
                        self.direction_command = 2
                    if event.key == pygame.K_DOWN:
                        self.direction_command = 3
                    if event.key == pygame.K_p:
                        self.toggle_pause()
                    elif event.key == pygame.K_q:
                        background = ChooseMode.ChooseMode()
                        background.run_menu()
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_SPACE and (self.game_over or self.game_won):
                        self.powerup = False
                        self.power_counter = 0
                        self.lives -= 1
                        self.startup_counter = 0
                        self.player_x = 450
                        self.player_y = 663
                        self.direction = 0
                        self.direction_command = 0
                        self.blinky_x = 56
                        self.blinky_y = 58
                        self.blinky_direction = 0
                        self.inky_x = 440
                        self.inky_y = 388
                        self.inky_direction = 2
                        self.pinky_x = 440
                        self.pinky_y = 438
                        self.pinky_direction = 2
                        self.clyde_x = 440
                        self.clyde_y = 438
                        self.clyde_direction = 2
                        self.eaten_ghost = [False, False, False, False]
                        self.blinky_dead = False
                        self.inky_dead = False
                        self.clyde_dead = False
                        self.pinky_dead = False
                        self.score = 0
                        self.lives = 3
                        self.level = copy.deepcopy(matrix)
                        self.game_over = False
                        self.game_won = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT and self.direction_command == 0:
                        self.direction_command = self.direction
                    if event.key == pygame.K_LEFT and self.direction_command == 1:
                        self.direction_command = self.direction
                    if event.key == pygame.K_UP and self.direction_command == 2:
                        self.direction_command = self.direction
                    if event.key == pygame.K_DOWN and self.direction_command == 3:
                        self.direction_command = self.direction

            if self.direction_command == 0 and self.turns_allowed[0]:
                self.direction = 0
            if self.direction_command == 1 and self.turns_allowed[1]:
                self.direction = 1
            if self.direction_command == 2 and self.turns_allowed[2]:
                self.direction = 2
            if self.direction_command == 3 and self.turns_allowed[3]:
                self.direction = 3

            if self.player_x > 900:
                self.player_x = -47
            elif self.player_x < -50:
                self.player_x = 897

            if blinky.in_box and self.blinky_dead:
                self.blinky_dead = False
            if inky.in_box and self.inky_dead:
                self.inky_dead = False
            if pinky.in_box and self.pinky_dead:
                self.pinky_dead = False
            if clyde.in_box and self.clyde_dead:
                self.clyde_dead = False

            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    pacman_game = PacmanGame()
    pacman_game.run_game()