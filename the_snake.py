"""
Игра 'Змейка' на Pygame.
Змейка ползает по полю, ест яблоки и растет.
При столкновении с собой игра начинается заново.
"""

import random

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость:
SPEED = 20

# Настройка окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=None, color=None):
        """Инициализация базового игрового объекта."""
        if position is None:
            position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.position = position
        self.body_color = color

    def draw(self):
        """Абстрактный метод отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс яблока, которое ест змейка."""

    def __init__(self, snake_positions=None):
        """Инициализация яблока."""
        super().__init__(color=APPLE_COLOR)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """Устанавливает случайное положение яблока."""
        if snake_positions is None:
            snake_positions = []

        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_positions:
                self.position = (x, y)
                break

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки, управляемой игроком."""

    def __init__(self):
        """Инициализация змейки в начальном состоянии."""
        super().__init__(color=SNAKE_COLOR)
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.positions = [(center_x, center_y)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, ate_apple=False):
        """Обновляет позицию змейки, добавляя новую голову."""
        head = self.get_head_position()
        new_head = (
            head[0] + self.direction[0],
            head[1] + self.direction[1]
        )

        x, y = new_head
        if x >= GRID_WIDTH:
            x = 0
        elif x < 0:
            x = GRID_WIDTH - 1
        elif y >= GRID_HEIGHT:
            y = 0
        elif y < 0:
            y = GRID_HEIGHT - 1
        new_head = (x, y)

        self.positions.insert(0, new_head)

        if not ate_apple:
            self.last = self.positions.pop()
        else:
            self.last = None
            self.length += 1

    def check_collision(self):
        """Проверяет, столкнулась ли змейка с собой."""
        head = self.get_head_position()
        return head in self.positions[1:]

    def draw(self):
        """Отрисовывает змейку на игровом поле и затирает след."""
        for position in self.positions:
            rect = pygame.Rect(
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                self.last[0] * GRID_SIZE,
                self.last[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры. Содержит главный игровой цикл."""
    pygame.init()

    snake = Snake()
    apple = Apple(snake.positions)
    font = pygame.font.Font(None, 36)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()

        ate_apple = False
        if snake.get_head_position() == apple.position:
            ate_apple = True
            apple.randomize_position(snake.positions)

        snake.move(ate_apple)

        if snake.check_collision():
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        score = snake.length - 1
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.update()


if __name__ == '__main__':
    main()