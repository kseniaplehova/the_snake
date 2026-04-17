"""
Игра 'Змейка' на Pygame.
Змейка ползает по полю, ест яблоки и растет.
При столкновении с собой игра начинается заново.
"""

import random

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Аннотации типов:
Pointer = tuple[int, int]

# Направления движения:
UP: Pointer = (0, -1)
DOWN: Pointer = (0, 1)
LEFT: Pointer = (-1, 0)
RIGHT: Pointer = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR: tuple[int, int, int] = (0, 0, 0)
BORDER_COLOR: tuple[int, int, int] = (93, 216, 228)
APPLE_COLOR: tuple[int, int, int] = (255, 0, 0)
SNAKE_COLOR: tuple[int, int, int] = (0, 255, 0)

# Скорость:
SPEED: int = 20

# Настройка окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    DEFAULT_COLOR: tuple[int, int, int] = (255, 255, 255)

    def __init__(
            self,
            position: tuple[int, int] | None = None,
            body_color: tuple[int, int, int] | None = None
    ) -> None:
        """Инициализация базового игрового объекта."""
        if position is None:
            position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.position = position
        self.body_color = (
            body_color if body_color is not None else self.DEFAULT_COLOR
        )

    def draw(self) -> None:
        """Абстрактный метод отрисовки объекта."""
        raise NotImplementedError(
            'Метод draw должен быть реализован в наследнике'
        )


class Apple(GameObject):
    """Класс яблока, которое ест змейка."""

    APPLE_COLOR: tuple[int, int, int] = (255, 0, 0)

    def __init__(
            self,
            occupied_positions: list[tuple[int, int]] | None = None,
            body_color: tuple[int, int, int] | None = None
    ) -> None:
        """Инициализация яблока."""
        if body_color is None:
            body_color = self.APPLE_COLOR
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(
            self,
            occupied_positions: list[tuple[int, int]] | None
    ) -> None:
        """Устанавливает случайное положение яблока."""
        if occupied_positions is None:
            occupied_positions = []

        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in occupied_positions:
                self.position = (x, y)
                break

    def draw(self) -> None:
        """Отрисовывает яблоко на игровом поле."""
        rect = pg.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE,
        )
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки, управляемой игроком."""

    SNAKE_COLOR: tuple[int, int, int] = (0, 255, 0)

    def __init__(
            self,
            body_color: tuple[int, int, int] | None = None,
            grid_width: int | None = None,
            grid_height: int | None = None
    ) -> None:
        """Инициализация змейки в начальном состоянии."""
        if body_color is None:
            body_color = self.SNAKE_COLOR
        super().__init__(body_color=body_color)
        self.grid_width = grid_width if grid_width is not None else GRID_WIDTH
        self.grid_height = (
            grid_height if grid_height is not None else GRID_HEIGHT
        )
        self.reset()

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        center_x = self.grid_width // 2
        center_y = self.grid_height // 2
        self.positions: list[tuple[int, int]] = [(center_x, center_y)]
        self.length: int = 1
        self.direction: Pointer = RIGHT
        self.next_direction: Pointer | None = None
        self.last: tuple[int, int] | None = None

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Обновляет позицию змейки, добавляя новую голову и убирая хвост."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        new_x = (head_x + dir_x) % self.grid_width
        new_y = (head_y + dir_y) % self.grid_height
        new_head = (new_x, new_y)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def grow(self) -> None:
        """Увеличивает длину змейки."""
        self.length += 1

    def check_collision(self) -> bool:
        """Проверяет, столкнулась ли змейка с собой."""
        return self.get_head_position() in self.positions[1:]

    def draw(self) -> None:
        """Отрисовывает змейку на игровом поле и затирает след."""
        for position in self.positions:
            rect = pg.Rect(
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pg.Rect(
                self.last[0] * GRID_SIZE,
                self.last[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake: Snake) -> None:
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main() -> None:
    """Основная функция игры. Содержит главный игровой цикл."""
    pg.init()

    snake = Snake(grid_width=GRID_WIDTH, grid_height=GRID_HEIGHT)
    apple = Apple(occupied_positions=snake.positions)
    font = pg.font.Font(None, 36)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        if snake.check_collision():
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        score = snake.length - 1
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pg.display.update()


if __name__ == '__main__':
    main()
