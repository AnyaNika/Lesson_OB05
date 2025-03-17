import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600  # Размеры окна
LIGHT_GRAY = (200, 200, 300)  # Цвет фона
GREEN = (200, 255, 200)  # Цвет игрока
DARK_BLUE = (0, 0, 200)  # Цвет блоков
WHITE = (255, 255, 255)  # Цвет текста

# Настройки окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Избегай падающих блоков!")

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)  # Устанавливаем цвет игрока в зеленый
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 30)  # Начальная позиция игрока

    def update(self):
        keys = pygame.key.get_pressed()  # Получаем нажимаемые клавиши
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5  # Движение влево
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5  # Движение вправо

# Класс падающего блока
class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(DARK_BLUE)  # Устанавливаем цвет блока в темно-синий
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)  # Случайная начальная позиция по x
        self.rect.y = random.randint(-100, -40)  # Случайная начальная позиция по y
        self.speedy = random.randint(3, 4)  # Случайная скорость падения

    def update(self):
        self.rect.y += self.speedy  # Движение блока вниз
        if self.rect.top > HEIGHT:  # Если блок выходит за нижнюю границу
            self.rect.x = random.randint(0, WIDTH - self.rect.width)  # Перемещаем его наверх
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(3, 4)

# Функция для отображения текста
def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Основной игровой цикл
def main():
    # Создание групп спрайтов
    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    for _ in range(8):
        block = Block()
        all_sprites.add(block)
        blocks.add(block)

    # Переменные для игры
    running = True
    clock = pygame.time.Clock()

    # Игровой цикл
    while running:
        clock.tick(60)  # Устанавливаем FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Выход из игры

        # Обновление состояний
        all_sprites.update()

        # Проверка столкновений
        if pygame.sprite.spritecollideany(player, blocks):
            # Если игрок сталкивается с блоком
            running = False  # Останавливаем основной игровой цикл
            game_over_screen()  # Переходим к экрану окончания игры

        # Отрисовка
        screen.fill(LIGHT_GRAY)  # Заполняем фон светло-серым
        all_sprites.draw(screen)  # Рисуем все спрайты
        pygame.display.flip()  # Обновляем экран

    pygame.quit()

# Функция для отображения экрана окончания игры
def game_over_screen():
    game_over = True
    while game_over:
        screen.fill(LIGHT_GRAY)
        draw_text("Игра окончена", 70, WHITE, WIDTH // 2, HEIGHT // 3)
        draw_text("Играть заново", 50, WHITE, WIDTH // 2, HEIGHT // 2)
        draw_text("Выход", 50, WHITE, WIDTH // 2, HEIGHT // 1.5)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if WIDTH // 2 - 100 < mouse_x < WIDTH // 2 + 100:
                    if HEIGHT // 2 - 25 < mouse_y < HEIGHT // 2 + 25:
                        main()  # Перезапуск игры
                    elif HEIGHT // 1.5 - 25 < mouse_y < HEIGHT // 1.5 + 25:
                        game_over = False  # Выход из игры

if __name__ == "__main__":
    main()