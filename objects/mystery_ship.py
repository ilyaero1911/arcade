from objects.game_object import GameObject
import random
import pygame


class MysteryShip(GameObject):
    """Класс таинственного корабля"""

    def __init__(self, config):
        x = -config.mystery_width
        y = 30
        super().__init__(x, y, config.mystery_width, config.mystery_height)
        self.config = config
        self.speed = config.mystery_speed

    def update(self, dt):
        """Обновляет позицию корабля"""
        self.x += self.speed * dt

    def draw(self, surface, color):
        """Отрисовывает таинственный корабль"""
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))
        # Окна корабля
        window_size = self.width // 6
        for i in range(3):
            pygame.draw.rect(surface, (0, 0, 0),
                             (self.x + (i + 1) * window_size * 2 - window_size,
                              self.y + self.height // 2 - window_size // 2,
                              window_size, window_size))