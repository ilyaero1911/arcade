from objects.game_object import GameObject
import pygame


class Bullet(GameObject):
    """Класс пули"""

    def __init__(self, x, y, speed, is_player_bullet):
        super().__init__(x, y, 4, 10)
        self.speed = speed
        self.is_player_bullet = is_player_bullet

    def update(self, dt):
        """Обновляет позицию пули"""
        self.y += self.speed * dt

    def draw(self, surface, color):
        """Отрисовывает пулю"""
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))