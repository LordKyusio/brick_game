import pygame
from random import randint
from modules.abstract_mode import AbstractGameMode


class Car:
    def __init__(self, screen, px1, car_x, car_y):
        self.on_pixel = pygame.image.load('assets/graphics/active_pixel.png')
        self.screen = screen
        self.px1 = px1
        self.car_x = car_x
        self.car_y = car_y

    def display_car(self, car_x, car_y):
        car_positions = [self.px1 * 3, self.px1 * 6]
        for i in [-1, 1, 0]:
            self.screen.blit(self.on_pixel, ((car_positions[car_x] + self.px1 * i), (car_y + 1) * self.px1))
        for i in [-1, 1]:
            self.screen.blit(self.on_pixel, ((car_positions[car_x] + self.px1 * i), (car_y + 3) * self.px1))
        for i in [0, 2]:
            self.screen.blit(self.on_pixel, (car_positions[car_x], (car_y + i) * self.px1))


class EnemyCarController:
    def __init__(self, screen, px1):
        self.enemies = [
            Car(screen, px1, 0, 0),
            Car(screen, px1, 0, -8),
            Car(screen, px1, 1, -16)
        ]

    def spawn_cars(self):
        for enemy in self.enemies:
            enemy.car_y = 0 - 8 * self.enemies.index(enemy)
            enemy.car_x = randint(0, 1)

    def move(self, next_step):
        for enemy in self.enemies:
            enemy.car_y += next_step

            if enemy.car_y > 20:
                enemy.car_y = - 4
                enemy.car_x = randint(0, 1)
            enemy.display_car(
                enemy.car_x,
                enemy.car_y
            )


class RacerGame(AbstractGameMode):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.player_moved = True
        self.bound_position = 0

        self.player = Car(self.screen, self.px1, 0, 16)
        self.enemy_controller = EnemyCarController(self.screen, self.px1)

        self.score_text = self.font.render(str(self.score), True, (0, 0, 0))
        self.textRect = self.score_text.get_rect()
        self.textRect.center = (100, 100)

    def main_controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.is_turbo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and self.player.car_x != 1:
                    self.player.car_x = 1
                    self.player_moved = True
                if event.key == pygame.K_LEFT and self.player.car_x != 0:
                    self.player.car_x = 0
                    self.player_moved = True
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.is_turbo = True
                if event.key == pygame.K_RETURN:
                    self.is_turbo = False
                    self.is_pause = True
                if event.key == pygame.K_r:
                    self.running = False
                    self.main_menu = True

    def display_bound(self, pixel_change):
        self.bound_position += pixel_change
        if self.bound_position > 3:
            self.bound_position = 0
        for x in [0, self.px1 * 9]:
            for y in range(20):
                if y not in [self.bound_position, self.bound_position + 4,
                             self.bound_position + 8, self.bound_position + 12,
                             self.bound_position + 16]:
                    self.screen.blit(self.on_pixel, (x, y * self.px1))
                    self.screen.blit(self.on_pixel, (x, y * self.px1))

    def win_loose_controller(self, next_step):
        for enemy in self.enemy_controller.enemies:
            if enemy.car_x == self.player.car_x and (13 < enemy.car_y < 19):
                self.lives -= 1
                self.enemy_controller.spawn_cars()
                self.current_speed = self.start_speed
                self.speed_score = 0
                self.player_moved = True
                if self.lives < 0:
                    self.game_over(self.screen, self.clock)
            if enemy.car_x != self.player.car_x and (enemy.car_y == 19):
                if next_step:
                    self.score += 1
                    self.speed_score += 1
                    if self.speed_score == 100 and self.current_speed < 10:
                        self.current_speed += 1

    def mode_loop(self):
        while self.running is True:
            self.clock.tick(60)
            next_step = self.step_controller(self.current_speed, self.is_turbo)
            self.pause_mode(self.clock)
            self.main_controls()
            self.win_loose_controller(next_step)

            if self.player_moved or next_step:
                self.display_background(self.screen)
                self.enemy_controller.move(next_step)
                self.player.display_car(self.player.car_x, 16)
                self.display_bound(next_step)
                self.display_score()
                self.display_lives()
            pygame.display.update()
            self.player_moved = False
        return self.main_menu
