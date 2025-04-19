import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Размер окна и заголовок
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game Menu")


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        pass


# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
DARK_BLUE = (0, 0, 128)

# Шрифты
font = pygame.font.SysFont(None, 55)
font_small = pygame.font.SysFont(None, 40)

# Режимы игры
mode = "menu"

# Кнопки для меню
buttons = [
    pygame.Rect(300, 200, 200, 50),  # "Flappy Bird"
    pygame.Rect(300, 300, 200, 50),  # "Maze"
    pygame.Rect(300, 400, 200, 50)  # "Exit"
]
button_texts = ["Flappy Bird", "Maze", "Exit"]

# Фон
background = pygame.image.load('background laberint.png')  # Заменить на свой файл фона
background = pygame.transform.scale(background, (800, 600))

# Изображения персонажей
flappy_bird_img = pygame.image.load('hamster.png')  # Заменить на свой файл птицы
flappy_bird_img = pygame.transform.scale(flappy_bird_img, (50, 50))

maze_player_img = pygame.image.load('hamster.png')  # Заменить на свой файл персонажа лабиринта
maze_player_img = pygame.transform.scale(maze_player_img, (50, 50))


# Функция для отрисовки меню
def draw_menu():
    screen.fill(BLACK)  # Заполнение экрана черным
    screen.blit(background, (0, 0))  # Отображаем фон
    for i, rect in enumerate(buttons):
        # Рисуем кнопки
        color = ORANGE if rect.collidepoint(pygame.mouse.get_pos()) else DARK_BLUE
        pygame.draw.rect(screen, color, rect)

        # Отображаем текст на кнопках
        text = font.render(button_texts[i], True, WHITE)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)


# Функция для игры "Flappy Bird"
def flappy_game():
    bird_x = 100
    bird_y = 300
    bird_velocity = 0
    gravity = 0.9
    jump_strength = -10

    pipes = []
    pipes_rect = []
    pipe_width = 70
    pipe_height = random.randint(100, 400)
    pipe_gap = 150
    pipe_velocity = 5

    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)
        screen.blit(background, (0, 0))  # Отображаем фон
        screen.blit(flappy_bird_img, (bird_x, bird_y))  # Отображаем птицу

        # Добавляем новые трубы
        if len(pipes) == 0 or pipes[-1][0] < 600:
            pipe_height = random.randint(100, 400)
            pipes.append([800, pipe_height])

        # Двигаем трубы
        pipes = [[x - pipe_velocity, y] for x, y in pipes if x > -pipe_width]

        # Рисуем трубы
        for x, y in pipes:
            r_up = pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x, 0, pipe_width, y))
            r_down = pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x, y + pipe_gap, pipe_width, 600 - y - pipe_gap))
            pipes_rect.append(r_up)
            pipes_rect.append(r_down)

        # for p in pipes_rect:
        #     if p.colliderect()

        # Двигаем птицу
        bird_velocity += gravity
        bird_y += bird_velocity

        # Проверка столкновений
        if bird_y > 550 or bird_y < 0:
            break

        for x, y in pipes:
            if bird_x + 50 > x and bird_x < x + pipe_width:
                if bird_y < y or bird_y + 50 > y + pipe_gap:
                    break

        # Обработчик событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Прыжок при нажатии пробела
                    bird_velocity = jump_strength

        pygame.display.update()
        clock.tick(60)


# Функция для игры "Maze"
def maze_game():
    player_x = 100
    player_y = 100
    player_speed = 5

    maze_walls = [
        pygame.Rect(70, 150, 400, 20),
        pygame.Rect(250, 300, 400, 20),
        pygame.Rect(630,100, 20, 200),
        pygame.Rect(70, 150, 20, 200),
        pygame.Rect(70, 320, 20, 200),
        pygame.Rect(70, 500, 400, 20),
        pygame.Rect(300, 500, 400, 20),
    ]

    # Финиш
    finish_rect = pygame.Rect(750, 550, 50, 50)

    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)
        screen.blit(background, (0, 0))  # Отображаем фон
        screen.blit(maze_player_img, (player_x, player_y))  # Отображаем персонажа

        # Рисуем стены лабиринта
        for wall in maze_walls:
            pygame.draw.rect(screen, (255, 0, 0), wall)

        # Рисуем финиш
        pygame.draw.rect(screen, (0, 255, 0), finish_rect)

        # Обработчик событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

        # Проверка на столкновения с стенами
        player_rect = pygame.Rect(player_x, player_y, 50, 50)
        for wall in maze_walls:
            if player_rect.colliderect(wall):
                # В случае столкновения, вернем игрока назад
                if keys[pygame.K_LEFT]:
                    player_x += player_speed
                if keys[pygame.K_RIGHT]:
                    player_x -= player_speed
                if keys[pygame.K_UP]:
                    player_y += player_speed
                if keys[pygame.K_DOWN]:
                    player_y -= player_speed

        # Проверка на достижение финиша
        if player_rect.colliderect(finish_rect):
            # Отображаем сообщение о победе
            text = font.render("You Win!", True, WHITE)
            screen.blit(text, (300, 250))
            pygame.display.update()
            pygame.time.wait(2000)  # Ждем 2 секунды перед возвратом в меню
            return

        pygame.display.update()
        clock.tick(60)


# Главный цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обработка кликов мыши на кнопках
        if event.type == pygame.MOUSEBUTTONDOWN:
            if buttons[0].collidepoint(event.pos):
                mode = "flappy"
            elif buttons[1].collidepoint(event.pos):
                mode = "maze"
            elif buttons[2].collidepoint(event.pos):
                running = False  # Выход из игры

    if mode == "menu":
        draw_menu()
    elif mode == "flappy":
        flappy_game()
    elif mode == "maze":
        maze_game()

    pygame.display.update()

pygame.quit()
sys.exit()
