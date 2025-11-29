import pygame
from objects.game_object import GameObject

class Bullet(GameObject):
    """Класс пули"""

    def __init__(self, x, y, speed, is_player_bullet, diagonal_direction=0):
        super().__init__(x, y, 4, 10)
        self.speed = speed
        self.is_player_bullet = is_player_bullet
        self.diagonal_direction = diagonal_direction  # -1: влево, 0: прямо, 1: вправо

    def update(self, dt):
        """Обновляет позицию пули с учетом диагонального движения"""
        self.y += self.speed * dt

        # Диагональное движение для пуль с бонусом
        if self.diagonal_direction != 0:
            diagonal_speed = self.speed * 0.3  # Скорость диагонального смещения
            self.x += self.diagonal_direction * diagonal_speed * dt

    def draw(self, surface, color):
        """Отрисовывает пулю"""
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))