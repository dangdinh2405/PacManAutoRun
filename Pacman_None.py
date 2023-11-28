import copy
import ChooseMode
import Greedy
import Random
import matrix
import pygame
import math


class Ghost:
    def __init__(self, x_coord, y_coord, img, box, id, screen, powerup, eaten_ghost,spooked_img):
        self.spooked_img = spooked_img
        self.eaten_ghost = eaten_ghost
        self.powerup = powerup
        self.screen = screen
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.img = img
        self.in_box = box
        self.id = id
        self.draw()

    def draw(self):
        if (not self.powerup) or (self.eaten_ghost[self.id] and self.powerup):
            self.screen.blit(self.img, (self.x_pos, self.y_pos))
        elif self.powerup and not self.eaten_ghost[self.id]:
            self.screen.blit(self.spooked_img, (self.x_pos, self.y_pos))


class PacmanGame:
    def __init__(self):
        pygame.init()
        self.paused = False
        self.WIDTH = 900
        self.HEIGHT = 950
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.timer = pygame.time.Clock()
        self.fps = 300
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.level = copy.deepcopy(matrix.matrix)
        self.color = 'blue'
        self.PI = math.pi
        self.player_images = []
        for i in range(1, 5):
            self.player_images.append(pygame.transform.scale(pygame.image.load(f'pacman_image/{i}.png'), (45, 45)))
        self.blinky_img = pygame.transform.scale(pygame.image.load(f'ghost_images/red.png'), (45, 45))
        self.pinky_img = pygame.transform.scale(pygame.image.load(f'ghost_images/pink.png'), (45, 45))
        self.inky_img = pygame.transform.scale(pygame.image.load(f'ghost_images/blue.png'), (45, 45))
        self.clyde_img = pygame.transform.scale(pygame.image.load(f'ghost_images/orange.png'), (45, 45))
        self.spooked_img = pygame.transform.scale(pygame.image.load(f'ghost_images/powerup.png'), (45, 45))
        self.dead_img = pygame.transform.scale(pygame.image.load(f'ghost_images/dead.png'), (45, 45))

        self.power_counter = 0
        matrix_handler = Random.MatrixHandler()
        self.random_coordinate = matrix_handler.random_zero_coordinate()

        self.x = self.random_coordinate[0]
        self.y = self.random_coordinate[1]
        num1 = (self.HEIGHT - 50) // 32
        num2 = (self.WIDTH // 30)
        self.player_x = (self.y * num2 + (0.5 * num2)) - 23
        self.player_y = (self.x * num1 + (0.5 * num1)) - 24


        self.direction = 0
        self.blinky_x = 400
        self.blinky_y = 388
        self.blinky_direction = 0
        self.inky_x = 440
        self.inky_y = 388
        self.inky_direction = 2
        self.pinky_x = 440
        self.pinky_y = 438
        self.pinky_direction = 2
        self.clyde_x = 480
        self.clyde_y = 438
        self.clyde_direction = 2
        self.counter = 0
        self.flicker = False
        self.turns_allowed = [False, False, False, False]
        self.direction_command = 0
        self.player_speed = 2
        self.score = 0
        self.powerup = False
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
        self.eaten_ghost = [False, False, False, False]

        self.greedy = Greedy.Greedy()
        self.path, self.steps = self.greedy.optimal(self.random_coordinate)

    def draw_misc(self):
        score_text = self.font.render(f'Score: {self.score}', True, 'white')
        self.screen.blit(score_text, (10, 920))
        noti_text = self.font.render('Push "P" to Pause', True, 'yellow')
        quit_text = self.font.render('Push "Q" to Quit', True, 'red')
        self.screen.blit(noti_text, (500, 920))
        self.screen.blit(quit_text, (700, 920))
        if self.powerup:
            pygame.draw.circle(self.screen, 'blue', (140, 930), 15)
        if self.game_over:
            pygame.draw.rect(self.screen, 'white', [50, 200, 800, 300], 0, 10)
            pygame.draw.rect(self.screen, 'dark gray', [70, 220, 760, 260], 0, 10)
            gameover_text = self.font.render('Game over! Space bar to restart!', True, 'red')
            self.screen.blit(gameover_text, (100, 300))
        if self.game_won:
            pygame.draw.rect(self.screen, 'white', [50, 200, 800, 300], 0, 10)
            pygame.draw.rect(self.screen, 'dark gray', [70, 220, 760, 260], 0, 10)
            gameover_text = self.font.render('Victory! Space bar to restart!', True, 'green')
            self.screen.blit(gameover_text, (100, 300))

    def check_collisions(self, scor, power, power_count):
        num1 = (self.HEIGHT - 50) // 32
        num2 = self.WIDTH // 30
        if 0 < self.player_x < 870:
            if self.level[int(self.center_y // num1)][int(self.center_x // num2)] == 1:
                self.level[int(self.center_y // num1)][int(self.center_x // num2)] = 0
                scor += 10
            if self.level[int(self.center_y // num1)][int(self.center_x // num2)] == 2:
                self.level[int(self.center_y // num1)][int(self.center_x // num2)] = 0
                scor += 50
                power = True
                power_count = 0

        return scor, power, power_count

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
                    pygame.draw.arc(self.screen, self.color,
                                    [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                    0, self.PI / 2, 3)
                if self.level[i][j] == 6:
                    pygame.draw.arc(self.screen, self.color,
                                    [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], self.PI / 2,
                                    self.PI, 3)
                if self.level[i][j] == 7:
                    pygame.draw.arc(self.screen, self.color,
                                    [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], self.PI,
                                    3 * self.PI / 2, 3)
                if self.level[i][j] == 8:
                    pygame.draw.arc(self.screen, self.color,
                                    [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1],
                                    3 * self.PI / 2,
                                    2 * self.PI, 3)
                if self.level[i][j] == 9:
                    pygame.draw.line(self.screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                     (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

    def draw_player(self):
        # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
        if self.direction == 0:
            self.screen.blit(self.player_images[self.counter // 5], (self.player_x, self.player_y))
        elif self.direction == 1:
            self.screen.blit(pygame.transform.flip(self.player_images[self.counter // 5], True, False),
                             (self.player_x, self.player_y))
        elif self.direction == 2:
            self.screen.blit(pygame.transform.rotate(self.player_images[self.counter // 5], 90),
                             (self.player_x, self.player_y))
        elif self.direction == 3:
            self.screen.blit(pygame.transform.rotate(self.player_images[self.counter // 5], 270),
                             (self.player_x, self.player_y))

    def check_position(self, centerx, centery):
        turns = [False, False, False, False]
        num1 = (self.HEIGHT - 50) // 32
        num2 = (self.WIDTH // 30)
        num3 = 15

        if centerx // 30 < 29:
            if self.direction == 0:
                if self.level[int(centery // num1)][int((centerx - num3) // num2)] < 3:
                    turns[1] = True
            elif self.direction == 1:
                if self.level[int(centery // num1)][int((centerx + num3) // num2)] < 3:
                    turns[0] = True
            elif self.direction == 2:
                if self.level[int((centery + num3) // num1)][int(centerx // num2)] < 3:
                    turns[3] = True
            elif self.direction == 3:
                if self.level[int((centery - num3) // num1)][int(centerx // num2)] < 3:
                    turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= centerx % num2 <= 18:
                    if self.level[int((centery + num3) // num1)][int(centerx // num2)] < 3:
                        turns[3] = True
                    if self.level[int((centery - num3) // num1)][int(centerx // num2)] < 3:
                        turns[2] = True
                if 12 <= centery % num1 <= 18:
                    if self.level[int(centery // num1)][int((centerx - num2) // num2)] < 3:
                        turns[1] = True
                    if self.level[int(centery // num1)][int((centerx + num2) // num2)] < 3:
                        turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= centerx % num2 <= 18:
                    if self.level[int((centery + num1) // num1)][int(centerx // num2)] < 3:
                        turns[3] = True
                    if self.level[int((centery - num1) // num1)][int(centerx // num2)] < 3:
                        turns[2] = True
                if 12 <= centery % num1 <= 18:
                    if self.level[int(centery // num1)][int((centerx - num3) // num2)] < 3:
                        turns[1] = True
                    if self.level[int(centery // num1)][int((centerx + num3) // num2)] < 3:
                        turns[0] = True
        else:
            turns[0] = True
            turns[1] = True

        return turns

    def move_pacman(self, player_x, player_y, x, y):
        player_x = player_x + 23
        player_y = player_y + 24

        new_x, new_y = player_x, player_y
        if self.path:
            if self.path[0] == self.path[-1]:
                new_x, new_y = player_x, player_y
            else:
                dx, dy = self.path[0]
                dx1, dy1 = self.path[1]
                if dy1 - dy == 1 and dx1 - dx == 0:
                    new_x = player_x + 1 * self.player_speed
                    self.direction = 0
                elif dy1 - dy == -1 and dx1 - dx == 0:
                    new_x = player_x + -1 * self.player_speed
                    self.direction = 1
                if dx1 - dx == -1 and dy1 - dy == 0:
                    new_y = player_y + -1 * self.player_speed
                    self.direction = 2
                elif dx1 - dx == 1 and dy1 - dy == 0:
                    new_y = player_y + 1 * self.player_speed
                    self.direction = 3
                if new_x == self.greedy.cd_array[dx1][dy1][0] and new_y == self.greedy.cd_array[dx1][dy1][1]:
                    x, y = dx1, dy1
                    self.path.pop(0)
        new_x = new_x - 23
        new_y = new_y - 24
        return new_x, new_y, x, y, self.direction

    def toggle_pause(self):
        self.paused = not self.paused
    def run(self):
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
                if self.startup_counter < 180 and not self.game_over and not self.game_won:
                    self.moving = False
                    self.startup_counter += 1
                else:
                    self.moving = True

                if self.moving:
                    self.player_x, self.player_y, self.x, self.y, self.direction = self.move_pacman(self.player_x,
                                                                                                    self.player_y,
                                                                                                    self.x, self.y)

            self.timer.tick(self.fps)
            self.screen.fill('black')
            self.draw_board()
            self.center_x = self.player_x + 23
            self.center_y = self.player_y + 24
            self.game_won = True
            for i in range(len(self.level)):
                if 1 in self.level[i] or 2 in self.level[i]:
                    self.game_won = False

            self.player_circle = pygame.draw.circle(self.screen, 'black', (self.center_x, self.center_y), 20, 2)
            self.draw_player()
            # x_coord, y_coord, img, box, id, screen, powerup, eaten_ghost, spooked_img
            blinky = Ghost(self.blinky_x, self.blinky_y, self.blinky_img, self.blinky_box, 0, self.screen, self.powerup, self.eaten_ghost, self.spooked_img)
            inky = Ghost(self.inky_x, self.inky_y, self.inky_img, self.inky_box, 1, self.screen, self.powerup, self.eaten_ghost, self.spooked_img)
            pinky = Ghost(self.pinky_x, self.pinky_y, self.pinky_img, self.pinky_box, 2, self.screen, self.powerup, self.eaten_ghost, self.spooked_img)
            clyde = Ghost(self.clyde_x, self.clyde_y, self.clyde_img, self.clyde_box, 3, self.screen, self.powerup, self.eaten_ghost, self.spooked_img)
            self.draw_misc()
            self.turns_allowed = self.check_position(self.center_x, self.center_y)

            self.score, self.powerup, self.power_counter = self.check_collisions(self.score, self.powerup, self.power_counter)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
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

            pygame.display.flip()

        pygame.quit()

# Run the game
if __name__ == "__main__":
    pacman_game = PacmanGame()
    pacman_game.run()