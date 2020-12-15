import pygame
from random import randint
from modules import racer_mode


class MenuAnimations:
    def __init__(self, screen, px1):
        self.screen = screen
        self.px1 = px1
        self.car = racer_mode.Car(screen, px1, 0, 16)
        self.next_step = True
        self.on_pixel = pygame.image.load('assets/graphics/active_pixel.png')

    def racer_animation(self):
        if self.next_step:
            self.car.car_x = randint(0, 1)
        for y in [2, 7]:
            for x in range(2, 7):
                self.screen.blit(self.on_pixel, (self.px1 * x, self.px1 * y))
        for x in [2, 7]:
            for y in range(3, 13):
                if y != 7:
                    self.screen.blit(self.on_pixel, (self.px1 * x, self.px1 * y))
        self.car.display_car(self.car.car_x, 16)
