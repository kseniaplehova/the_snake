import random
import pygame

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
SPEED = 10  # Уменьшил скорость для удобства

# Настройка окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.positions = [
            (GRID_WIDTH // 2, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2),
        ]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def move(self, ate_apple=False):
        head = self.positions[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

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
        if ate_apple:
            self.last = None
        else:
            self.last = self.positions.pop()

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def check_collision(self):
        return self.positions[0] in self.positions[1:]

    def draw(self):
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_pos = self.positions[0]
        head_rect = pygame.Rect(
            head_pos[0] * GRID_SIZE,
            head_pos[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                self.last[0] * GRID_SIZE,
                self.last[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


class Apple:
    def __init__(self, snake_positions):
        self.body_color = APPLE_COLOR
        self.position = (0, 0)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_positions:
                self.position = (x, y)
                break

    def draw(self):
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(snake):
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
    pygame.init()
    
    snake = Snake()
    apple = Apple(snake.positions)
    score = 0
    font = pygame.font.Font(None, 36)
    
    while True:
        clock.tick(SPEED)
        
        handle_keys(snake)
        snake.update_direction()
        
        ate_apple = False
        if snake.positions[0] == apple.position:
            ate_apple = True
            score += 1
            apple.randomize_position(snake.positions)
        
        snake.move(ate_apple)
        
        if snake.check_collision():
            print(f"Game Over! Score: {score}")
            pygame.quit()
            raise SystemExit
        
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        pygame.display.update()


if __name__ == "__main__":
    main()