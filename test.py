import copy
from matrix import matrix
import pygame
import math
import AStar
import DFS
import BFS



pygame.init()
WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(matrix)
color = 'blue'
PI = math.pi
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'pacman_image/{i}.png'), (45, 45)))

icon = pygame.image.load("pacman_image/1.png")
pygame.display.set_icon(icon)

player_x = 75 - 23
player_y = 70 - 24
direction = 0

x, y = 2, 2

counter = 0
flicker = False
# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0

targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]

moving = False

ghost_speeds = [2, 2, 2, 2]
startup_counter = 0

lives = 3
game_over = False
game_won = False


def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))


def check_collisions(scor, power, power_count):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            power = True
            power_count = 0
    return scor, power, power_count


def draw_board():
    num1 = (HEIGHT - 50) // 32 #28
    num2 = (WIDTH // 30) #30
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15

    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True

        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(play_x, play_y):
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y

dfs = DFS.DFS()
path = dfs.optimal()
def move_pacman(player_x, player_y, x, y):
    global direction
    player_x = player_x + 23
    player_y = player_y + 24

    # start = (x, y)
    # goal = (30, 2)
    #
    # solver = AStar.AStar(start, goal)
    # path = solver.astar()
    # print(path)

    print(path)
    end_dx = path[-1][0]
    end_dy = path[-1][1]

    new_x, new_y = player_x, player_y
    if path:
        if path[0] == path[-1]:
            new_x, new_y = player_x, player_y
        else:
            dx, dy = path[0]
            dx1, dy1 = path[1]
            if dy1 - dy == 1 and dx1 - dx == 0:
                new_x = player_x + 1 * player_speed
                direction = 0
            elif dy1 - dy == -1 and dx1 - dx == 0:
                new_x = player_x + -1 * player_speed
                direction = 1
            if dx1 - dx == -1 and dy1 - dy == 0:
                new_y = player_y + -1 * player_speed
                direction = 2
            elif dx1 - dx == 1 and dy1 - dy == 0:
                new_y = player_y + 1 * player_speed
                direction = 3
            if new_x == dfs.cd_array[dx1][dy1][0] and new_y == dfs.cd_array[dx1][dy1][1]:
                x, y = dx1, dy1
                path.pop(0)

    new_x = new_x - 23
    new_y = new_y - 24
    print(new_x, new_y)
    return new_x, new_y, x, y, direction


run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill('black')
    draw_board()
    center_x = player_x + 23
    center_y = player_y + 24

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)
    draw_player()
    draw_misc()

    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y, x, y, direction = move_pacman(player_x, player_y, x, y)
        # player_x, player_y = move_player(player_x, player_y)
        # print(player_x, player_y)

    score, powerup, power_counter = check_collisions(score, powerup, power_counter)
    # add to if not powerup to check if eaten ghosts

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         run = False
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_RIGHT:
    #             direction_command = 0
    #         if event.key == pygame.K_LEFT:
    #             direction_command = 1
    #         if event.key == pygame.K_UP:
    #             direction_command = 2
    #         if event.key == pygame.K_DOWN:
    #             direction_command = 3
    #         if event.key == pygame.K_SPACE and (game_over or game_won):
    #             powerup = False
    #             power_counter = 0
    #             lives -= 1
    #             startup_counter = 0
    #             player_x = 450
    #             player_y = 663
    #             direction = 0
    #             direction_command = 0
    #             score = 0
    #             lives = 3
    #             level = copy.deepcopy(matrix)
    #             game_over = False
    #             game_won = False
    #
    #     if event.type == pygame.KEYUP:
    #         if event.key == pygame.K_RIGHT and direction_command == 0:
    #             direction_command = direction
    #         if event.key == pygame.K_LEFT and direction_command == 1:
    #             direction_command = direction
    #         if event.key == pygame.K_UP and direction_command == 2:
    #             direction_command = direction
    #         if event.key == pygame.K_DOWN and direction_command == 3:
    #             direction_command = direction


    # if direction_command == 0 and turns_allowed[0]:
    #     direction = 0
    # if direction_command == 1 and turns_allowed[1]:
    #     direction = 1
    # if direction_command == 2 and turns_allowed[2]:
    #     direction = 2
    # if direction_command == 3 and turns_allowed[3]:
    #     direction = 3

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    pygame.display.flip()
pygame.quit()