# The Snake

The classic Snake game written with Pygame and an object-oriented design.

Educational project — Yandex Practicum, Python Developer course.

## Features

- Class hierarchy: `GameObject` (base class with abstract `draw()`), with `Apple` and `Snake` as subclasses.
- Grid-based 640x480 field with 20 px cells; the snake wraps around the screen edges.
- Arrow-key control; reversing straight into the snake's own body is blocked.
- The snake grows after eating an apple; apples spawn only on free cells.
- Colliding with itself resets the game; the current score is shown on screen.
- Type annotations and docstrings throughout, checked with flake8.

## Tech stack

Python 3.10+ (uses `X | None` type syntax), Pygame 2.5.2, pytest, flake8 (see `requirements.txt`).

## Getting started

```bash
git clone https://github.com/kseniaplehova/the_snake.git
cd the_snake
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash); on Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python the_snake.py
```

## Tests

```bash
pytest
```

## Author

Ksenia Plehova — [GitHub](https://github.com/kseniaplehova)
