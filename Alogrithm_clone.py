import pygame

import PacMan_AStart
import PacMan_BFS
import PacMan_DFS
import PacMan_Greedy
import ChooseMode
import time

import PacMan_UCS


class AlgorithmClone:
    def __init__(self):
        self.WIDTH = 950
        self.HEIGHT = 900
        pygame.mixer.init()
        pygame.mixer.music.load("audio/play_main.mp3")
        pygame.mixer.music.play()

        pygame.init()
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.timer = pygame.time.Clock()
        self.fps = 60

        # Icon của các cửa sổ
        icon = pygame.image.load('Graphics/Icon_Snake.png')
        pygame.display.set_icon(icon)

        pygame.display.set_caption("Trò chơi Pacman")

        # CỬA SỔ START
        self.root = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        background = pygame.image.load('Graphics/Alogrithm.png')
        background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
        self.root.blit(background, (0, 0))

        # Tạo nút "BFS"
        self.bfs_button = pygame.Rect(230, 590, 250, 50)
        self.button_color = pygame.Color("#000000")
        self.hover_color = pygame.Color("#333333")

        # Tạo nút "DFS"
        self.dfs_button = pygame.Rect(230, 520, 250, 50)
        self.dfs_button_color = pygame.Color("#000000")
        self.dfs_hover_color = pygame.Color("#333333")

        # Tạo nút "Greedy"
        self.greedy_button = pygame.Rect(230, 650, 250, 50)
        self.greedy_button_color = pygame.Color("#000000")
        self.greedy_hover_color = pygame.Color("#333333")

        # Tạo nút "Back"
        self.back_button = pygame.Rect(350, 740, 250, 50)
        self.back_button_color = pygame.Color("#000000")
        self.back_hover_color = pygame.Color("#333333")

        # Tạo nút "Astart"
        self.astart_button = pygame.Rect(530, 570, 250, 50)
        self.astart_button_color = pygame.Color("#000000")
        self.astart_over_color = pygame.Color("#333333")

        # Tạo nút "UCS"
        self.ucs_button = pygame.Rect(530, 650, 250, 50)
        self.ucs_button_color = pygame.Color("#000000")
        self.ucs_hover_color = pygame.Color("#333333")

        self.font = pygame.font.Font("Graphics/Font.ttf", 50)

    def run_menu_algorithm_clone(self):
        running = True
        while running:
            self.timer.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.bfs_button.collidepoint(mouse_pos):
                        pygame.mixer.music.pause()
                        time.sleep(1)
                        pacman_game = PacMan_BFS.PacmanGame()
                        pygame.mixer.init()
                        pygame.mixer.music.load("audio/game_start.mp3")
                        pygame.mixer.music.play()
                        pacman_game.run_game()
                        pygame.quit()
                        quit()
                    elif self.dfs_button.collidepoint(mouse_pos):
                        pygame.mixer.music.pause()
                        time.sleep(1)
                        pacman_game = PacMan_DFS.PacmanGame()
                        pygame.mixer.init()
                        pygame.mixer.music.load("audio/game_start.mp3")
                        pygame.mixer.music.play()
                        pacman_game.run_game()
                        pygame.quit()
                        quit()
                    elif self.greedy_button.collidepoint(mouse_pos):
                        pygame.mixer.music.pause()
                        time.sleep(1)
                        pacman_game = PacMan_Greedy.PacmanGame()
                        pygame.mixer.music.load("audio/game_start.mp3")
                        pygame.mixer.music.play()
                        pacman_game.run_game()
                        pygame.quit()
                        quit()
                    elif self.astart_button.collidepoint(mouse_pos):
                        pygame.mixer.music.pause()
                        time.sleep(1)
                        pacman_game = PacMan_AStart.PacmanGame()
                        pygame.mixer.music.load("audio/game_start.mp3")
                        pygame.mixer.music.play()
                        pacman_game.run_game()
                        pygame.quit()
                        quit()
                    elif self.ucs_button.collidepoint(mouse_pos):
                        pygame.mixer.music.pause()
                        time.sleep(1)
                        pacman_game = PacMan_UCS.PacmanGame()
                        pygame.mixer.music.load("audio/game_start.mp3")
                        pygame.mixer.music.play()
                        pacman_game.run_game()
                        pygame.quit()
                        quit()
                    elif self.back_button.collidepoint(mouse_pos):
                        background = ChooseMode.ChooseMode()
                        background.run_menu()
                        pygame.quit()
                        quit()

            mouse_pos = pygame.mouse.get_pos()

            if self.bfs_button.collidepoint(mouse_pos):
                bfs_color = self.hover_color
            else:
                bfs_color = self.button_color

            if self.dfs_button.collidepoint(mouse_pos):
                dfs_color = self.dfs_hover_color
            else:
                dfs_color = self.dfs_button_color

            if self.greedy_button.collidepoint(mouse_pos):
                greedy_color = self.greedy_hover_color
            else:
                greedy_color = self.greedy_button_color

            if self.astart_button.collidepoint(mouse_pos):
                astart_color = self.astart_over_color
            else:
                astart_color = self.astart_button_color

            if self.ucs_button.collidepoint(mouse_pos):
                ucs_color = self.ucs_hover_color
            else:
                ucs_color = self.ucs_button_color

            if self.back_button.collidepoint(mouse_pos):
                back_color = self.back_hover_color
            else:
                back_color = self.back_button_color



            pygame.draw.rect(self.root, bfs_color, self.bfs_button)
            pygame.draw.rect(self.root, dfs_color, self.dfs_button)
            pygame.draw.rect(self.root, greedy_color, self.greedy_button)
            pygame.draw.rect(self.root, back_color, self.back_button)
            pygame.draw.rect(self.root, astart_color, self.astart_button)
            pygame.draw.rect(self.root, ucs_color, self.ucs_button)

            bfs_text = self.font.render("BFS", True, "#FFD800")
            dfs_text = self.font.render("DFS", True, "#FFD800")
            greedy_text = self.font.render("Greedy", True, "#FFD800")
            back_text = self.font.render("Back", True, "#FFD800")
            astart_text = self.font.render("Astart", True, "#FFD800")
            ucs_text = self.font.render("UCS", True, "#FFD800")

            bfs_text_rect = bfs_text.get_rect(center=self.bfs_button.center)
            dfs_text_rect = dfs_text.get_rect(center=self.dfs_button.center)
            greedy_text_rect = greedy_text.get_rect(center=self.greedy_button.center)
            back_text_rect = back_text.get_rect(center=self.back_button.center)
            astart_text_rect = astart_text.get_rect(center=self.astart_button.center)
            ucs_text_rect = ucs_text.get_rect(center=self.ucs_button.center)

            self.root.blit(bfs_text, bfs_text_rect)
            self.root.blit(dfs_text, dfs_text_rect)
            self.root.blit(greedy_text, greedy_text_rect)
            self.root.blit(astart_text, astart_text_rect)
            self.root.blit(ucs_text, ucs_text_rect)
            self.root.blit(back_text, back_text_rect)

            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    pygame.init()  # Khởi tạo Pygame chỉ một lần ở đầu chương trình của bạn
    algorithm_clone = AlgorithmClone()
    algorithm_clone.run_menu_algorithm_clone()
    pygame.quit()  # Đảm bảo thoát Pygame khi trò chơi kết thúc
