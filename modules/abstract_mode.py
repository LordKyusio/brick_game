import pygame


class AbstractGameMode:
    def __init__(self, screen, clock, speed=1):
        pygame.init()

        # Graphics
        self.px1 = 24
        self.on_pixel = pygame.image.load('assets/graphics/active_pixel.png')
        self.off_pixel = pygame.image.load('assets/graphics/off_pixel.png')
        self.background_row = pygame.image.load('assets/graphics/empty_row.png')
        self.digit_font = pygame.font.Font('assets/fonts/Segment7/Segment7-4Gml.otf', 13)
        self.text_font = pygame.font.Font('assets/fonts/Open_Sans/OpenSans-SemiBold.ttf', 11)

        # pygame main
        self.screen = screen
        self.clock = clock

        # game variables
        self.tick = 0
        self.is_pause = False
        self.is_turbo = False
        self.main_menu = False
        self.running = True
        self.score = 0
        self.speed_score = 0
        self.lives = 4
        self.start_speed = speed
        self.current_speed = self.start_speed
        self.player_action = True

        # colors
        self.black = (0, 0, 0)
        self.off_black = (142, 152, 146)
        self.background = (151, 177, 165)

    def display_lives(self):
        for x in range(self.lives):
            self.screen.blit(self.on_pixel, (self.px1 * (x + 11), self.px1 * 4))

    def display_score(self):
        score_empty_text = self.digit_font.render("8888", True, self.off_black)
        speed_empty_text = self.digit_font.render("8", True, self.off_black)
        score_text = self.digit_font.render((4 - len(str(self.score))) * ' ' + str(self.score), True, self.black)
        speed_text = self.digit_font.render(str(self.current_speed), True, self.black)
        speed_title_text = self.text_font.render('SPEED', True, self.black)
        score_title_text = self.text_font.render('SCORE', True, self.black)

        score_rect = score_text.get_rect()
        speed_rect = speed_text.get_rect()
        speed_title_rect = score_text.get_rect()
        score_title_rect = speed_text.get_rect()

        score_rect.center = (13 * self.px1, 15 * self.px1)
        speed_rect.center = (13 * self.px1, 13 * self.px1)
        score_title_rect.center = (12.5 * self.px1, 14 * self.px1)
        speed_title_rect.center = (13 * self.px1, 12 * self.px1)

        self.screen.blit(speed_empty_text, speed_rect)
        self.screen.blit(score_empty_text, score_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(speed_text, speed_rect)
        self.screen.blit(score_title_text, score_title_rect)
        self.screen.blit(speed_title_text, speed_title_rect)

    def display_background(self, screen, start=0, stop=20):
        pause_text_off = self.text_font.render('PAUSE', True, self.off_black)
        pause_rect = pause_text_off.get_rect()
        pause_rect.center = (13 * self.px1, 16 * self.px1)
        screen.fill((151, 177, 165))
        for line in range(start, stop):
            screen.blit(self.background_row, (0, line * self.px1))
        for y in range(1, 5):
            for x in range(11, 15):
                self.screen.blit(self.off_pixel, (self.px1 * x, self.px1 * y))
        screen.blit(pause_text_off, pause_rect)

    def game_over(self, screen, clock, line=-1):
        self.tick = 0
        while line <= 20:
            clock.tick(60)
            step = self.step_controller(10, False)
            line += step
            if step:
                for pixel in range(0, 10):
                    screen.blit(self.on_pixel, (pixel * self.px1, line * self.px1))
                pygame.display.update()
        self.player_action = False
        self.main_menu = True
        self.running = False

    def pause_mode(self, clock):
        if self.is_pause:
            pause_text_on = self.text_font.render('PAUSE', True, self.black)
            pause_rect = pause_text_on.get_rect()
            pause_rect.center = (13 * self.px1, 16 * self.px1)
            self.screen.blit(pause_text_on, pause_rect)
            while self.is_pause:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.is_pause = False
                        if event.key == pygame.K_r:
                            self.running = False
                            self.main_menu = True
                pygame.display.update()
            self.player_action = True

    def step_controller(self, speed, is_turbo):
        self.tick += 1
        if not is_turbo:
            game_speed = 30/speed
        else:
            game_speed = 1.5
        if self.tick >= game_speed:
            self.tick = 0
            return True
        return False
