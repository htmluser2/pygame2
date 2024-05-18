import pygame
import os
import random
import time
import sys

pygame.init()

# Глобальні константи
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

VIDEO_PATH = "Assets/Videos/rickroll.mp4"

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5
    WIDTH = 44  # Нова ширина динозавра
    HEIGHT = 44  # Нова висота динозавра

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = pygame.Rect(self.X_POS, self.Y_POS, self.WIDTH, self.HEIGHT)  # Використовуємо власний прямокутник

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = pygame.Rect(self.X_POS, self.Y_POS_DUCK, self.WIDTH, self.HEIGHT)  # Змінюємо розмір прямокутника
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = pygame.Rect(self.X_POS, self.Y_POS, self.WIDTH, self.HEIGHT)  # Змінюємо розмір прямокутника
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load("music2.mp3")
    pygame.mixer.music.play(-1)  # Відтворювати музику в безкінечному циклі
    pygame.mixer.music.set_volume(0.5)  # Налаштування гучності


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, hight_score
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    # Отримання рекорду
    try:
        with open('hight_score.txt', 'r') as file:
            hight_score = int(file.read())
    except FileNotFoundError:
        hight_score = 0

    # Відтворення музики під час гри
    play_music()

    def score():
        global points, game_speed, hight_score
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

        # Оновлення рекорду
        if points > hight_score:
            hight_score = points
            with open('hight_score.txt', 'w') as file:
                file.write(str(hight_score))

        high_score_text = font.render("Hight Score: " + str(hight_score), True, (0, 0, 0))
        high_score_rect = high_score_text.get_rect()
        high_score_rect.center = (1000, 70)
        SCREEN.blit(high_score_text, high_score_rect)

    def background():
        global x_pos_bg, y_pos_bg
        for i in range(20):
            a = 1
        if points > 700:
            i = 0
            while i < 140:
                SCREEN.fill((i,i,i))
                i += 1
        if points > 100000000:
            d = a

        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()
        background()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)


        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(35)
        pygame.display.update()

# Константи для екрану
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Головне меню")

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Константи для кнопок
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = WHITE
BUTTON_BORDER_COLOR = BLACK
BUTTON_TEXT_COLOR = BLACK
BUTTON_TEXT_SIZE = 30

# Функція для створення кнопок
def create_button(text, x, y):
    font = pygame.font.SysFont(None, BUTTON_TEXT_SIZE)
    text_surface = font.render(text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + BUTTON_WIDTH / 2, y + BUTTON_HEIGHT / 2))
    pygame.draw.rect(SCREEN, BUTTON_BORDER_COLOR, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), 3)  # Додали обводку
    pygame.draw.rect(SCREEN, BUTTON_COLOR, (x+3, y+3, BUTTON_WIDTH-6, BUTTON_HEIGHT-6))  # Залили кнопку кольором
    SCREEN.blit(text_surface, text_rect)
    return text_rect

def main_menu():
    while True:
        SCREEN.fill(WHITE)
        
        # Створення кнопок
        play_button_rect = create_button("складність: легко", 500, 200)
        settings_button_rect = create_button("складність: важко", 500, 300)
        quit_button_rect = create_button("грати секретний режим", 450, 400)

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_button_rect.collidepoint(mouse_pos):
                    running = True
                    game_speed = 5
                    JUMP_VEL = 8.5
                    print("складність змінено на ЛЕГКО")
                    main()
                elif settings_button_rect.collidepoint(mouse_pos):
                    running = True
                    game_speed = 30
                    JUMP_VEL = 7.0
                    print("складність змінено на ВАЖКО")
                    main()
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()

        pygame.display.flip()

main_menu()

def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)

video = pygame.movie.Movie(VIDEO_PATH)

def play_video():
    video.play()

def stop_video():
    video.stop()

def main():
    run = True

    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r or event.key == pygame.K_R:
                    play_video()  # Відтворити відео при натисканні клавіші R
                if event.key == pygame.K_q:  # Запустити відео при натисканні клавіші Q
                    play_video()

        SCREEN.fill((0, 0, 0))
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()