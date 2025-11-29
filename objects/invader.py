import pygame
from objects.game_object import GameObject
from objects.bullet import Bullet
import random


class Invader(GameObject):
    """Класс пришельца"""

    def __init__(self, x, y, invader_type, config, points):
        super().__init__(x, y, config.invader_width, config.invader_height)
        self.config = config
        self.type = invader_type
        self.points = points
        self.direction = 1  # 1: вправо, -1: влево
        self.move_timer = 0
        self.move_interval = 1.0
        self.has_moved_down = False  # Флаг для отслеживания спуска

    def update(self, dt):
        """Обновляет позицию пришельца"""
        self.move_timer += dt
        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.x += self.direction * self.config.invader_horizontal_speed

    def should_move_down(self, invaders):
        """Проверяет, нужно ли пришельцам спускаться"""
        # Находим самого правого или левого пришельца в зависимости от направления
        if self.direction == 1:  # Движение вправо
            rightmost_x = max(inv.x + inv.width for inv in invaders)
            return rightmost_x >= self.config.window_width - 20
        else:  # Движение влево
            leftmost_x = min(inv.x for inv in invaders)
            return leftmost_x <= 20

    def move_down(self):
        """Спускает пришельца вниз"""
        self.y += self.config.invader_vertical_speed
        self.has_moved_down = True

    def change_direction(self):
        """Меняет направление движения"""
        self.direction *= -1
        self.has_moved_down = False

    def shoot(self):
        """Создает пулю пришельца"""
        bullet_x = self.x + self.width // 2 - 2
        bullet_y = self.y + self.height
        return Bullet(bullet_x, bullet_y, self.config.invader_bullet_speed, False)

    def draw(self, surface, color):
        """Отрисовывает пришельца"""
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))
        # Глаза
        eye_size = self.width // 5
        pygame.draw.rect(surface, (0, 0, 0), (self.x + eye_size, self.y + eye_size, eye_size, eye_size))
        pygame.draw.rect(surface, (0, 0, 0),
                         (self.x + self.width - 2 * eye_size, self.y + eye_size, eye_size, eye_size))