import pygame
from modules import racer_mode, menu_animations
from modules.abstract_mode import AbstractGameMode


class MainMenu(AbstractGameMode):
    def __init__(self):
        self.px1 = 24
        self.screen = pygame.display.set_mode((16 * self.px1, 20 * self.px1))
        self.clock = pygame.time.Clock()
        self.current_speed = 1
        super().__init__(self.screen, self.clock)
        pygame.display.set_caption("Brick Game")
        self.menu_animations = menu_animations.MenuAnimations(self.screen, self.px1)
        self.mode_loop()
        self.player_action = True

    def main_controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.running = racer_mode.RacerGame(self.screen, self.clock, self.current_speed).mode_loop()
                if event.key == pygame.K_DOWN and self.current_speed > 1:
                    self.current_speed -= 1
                    self.player_action = True
                if event.key == pygame.K_UP and self.current_speed < 9:
                    self.current_speed += 1
                    self.player_action = True

    def mode_loop(self):
        next_step = True
        x = 0
        while self.running:
            self.clock.tick(60)
            self.main_controls()
            if next_step or self.player_action:
                x += 1
                self.display_background(self.screen)
                self.display_score()
                self.menu_animations.next_step = next_step
                self.menu_animations.racer_animation()
            next_step = self.step_controller(1, False)

            pygame.display.update()
            self.player_action = False
