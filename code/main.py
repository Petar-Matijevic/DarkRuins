import pygame
import sys

from typer.colors import WHITE

from settings import *
from level import Level

class Game:
    def __init__(self):
        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Dark Ruins')
        self.clock = pygame.time.Clock()
        self.level = Level()

        # Sound
        main_song = pygame.mixer.Sound('../audio/main3.wav')
        main_song.set_volume(0.8)
        main_song.play(loops=-1)

        # Menu setup
        self.menu_font = pygame.font.Font(UI_FONT, 36)
        self.play_button = self.menu_font.render('Play', True, WHITE)
        self.exit_button = self.menu_font.render('Exit', True, WHITE)
        self.controls_button = self.menu_font.render('Input', True, WHITE)
        self.button_width = self.play_button.get_width() + 40
        self.button_height = self.play_button.get_height() + 20
        self.button_padding = 20
        self.button_margin = 50
        self.play_button_rect = pygame.Rect(
            (WIDTH - self.button_width) // 2,
            (HEIGTH - (self.button_height + self.button_padding + self.button_height + self.button_padding + self.button_margin)) // 2,
            self.button_width,
            self.button_height
        )
        self.controls_button_rect = self.play_button_rect.move(
            0,
            self.button_height + self.button_padding
        )
        self.exit_button_rect = self.controls_button_rect.move(
            0,
            self.button_height + self.button_padding + self.button_margin
        )

        # Background setup
        self.background = pygame.image.load('../graphics/Bacground/b1.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))

        # Controls popup setup
        self.controls_popup_font = pygame.font.Font(UI_FONT, 24)
        controls_text_lines = ['Movement: Arrow keys',
                               'Attack: Space bar',
                               'Magic: L_Shift',
                               'Change Weapon: R_Shift',
                               'Change Spell: L_CTRL',
                               'Upgrade Menu: d',
                               'Upgrade: e']
        line_height = self.controls_popup_font.get_linesize()
        controls_text_height = line_height * len(controls_text_lines)
        self.controls_popup_text = pygame.Surface((WIDTH, controls_text_height + line_height)).convert_alpha()
        self.controls_popup_text.fill((0, 0, 0, 0))
        for i, line in enumerate(controls_text_lines):
            text_surface = self.controls_popup_font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, (i * line_height) + (line_height // 2)))
            self.controls_popup_text.blit(text_surface, text_rect)

        self.controls_popup_rect = self.controls_popup_text.get_rect(center=(WIDTH // 2, HEIGTH // 2))
        self.controls_popup_active = False
        self.controls_popup_timer = 10

    def display_controls_popup(self):
        self.controls_popup_active = True
        self.controls_popup_timer = pygame.time.get_ticks()

    def return_to_menu(self):
        self.controls_popup_active = False

    def run(self):
        in_menu = True
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.level.toggle_menu()
                        if not self.level.menu_active:
                            self.return_to_menu()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if in_menu and event.button == 1:
                        if self.play_button_rect.collidepoint(event.pos):
                            in_menu = False
                            # Start the game here
                        elif self.exit_button_rect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                        elif self.controls_button_rect.collidepoint(event.pos):
                            self.display_controls_popup()

            self.screen.blit(self.background, (0, 0))

            if in_menu:
                pygame.draw.rect(self.screen, UI_BG_COLOR, self.play_button_rect)
                pygame.draw.rect(self.screen, UI_BG_COLOR, self.controls_button_rect)
                pygame.draw.rect(self.screen, UI_BG_COLOR, self.exit_button_rect)
                self.screen.blit(self.play_button, (self.play_button_rect.centerx - self.play_button.get_width() // 2,
                                                    self.play_button_rect.centery - self.play_button.get_height() // 2))
                self.screen.blit(self.controls_button, (self.controls_button_rect.centerx - self.controls_button.get_width() // 2,
                                                        self.controls_button_rect.centery - self.controls_button.get_height() // 2))
                self.screen.blit(self.exit_button, (self.exit_button_rect.centerx - self.exit_button.get_width() // 2,
                                                    self.exit_button_rect.centery - self.exit_button.get_height() // 2))
            else:
                self.level.run()

            if self.controls_popup_active:
                pygame.draw.rect(self.screen, UI_BG_COLOR, self.controls_popup_rect)
                self.screen.blit(self.controls_popup_text, (self.controls_popup_rect.centerx - self.controls_popup_text.get_width() // 2,
                                                            self.controls_popup_rect.centery - self.controls_popup_text.get_height() // 2))
                if pygame.time.get_ticks() - self.controls_popup_timer >= 10000:
                    self.return_to_menu()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
