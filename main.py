import pygame
import racer
from abstract_mode import AbstractGameMode


class MainMenu(AbstractGameMode):

    def __init__(self):
        self.px1 = 24
        self.screen = pygame.display.set_mode((16 * self.px1, 20 * self.px1))
        self.clock = pygame.time.Clock()
        super().__init__(self.screen, self.clock)
        pygame.display.set_caption("Brick Game")

    def main_controls(self):
        """temporary solution"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.running = racer.RacerGame(self.screen, self.clock).__main__()

    def __main__(self):
        next_step = True
        while self.running:
            self.clock.tick(60)
            if next_step:
                self.display_background(self.screen)
            next_step = self.step_controller(self.current_speed, self.is_turbo)
            self.main_controls()
            pygame.display.update()


MainMenu().__main__()
