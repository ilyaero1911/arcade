import pygame
class GameObject:
    """Базовый класс для всех игровых объектов"""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.active = True

    def update(self, dt):
        """Обновляет состояние объекта"""
        pass

    def draw(self, surface, color):
        """Отрисовывает объект"""
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        """Возвращает прямоугольник объекта для проверки столкновений"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_colliding_with(self, other_obj):
        """Проверяет столкновение с другим игровым объектом"""
        return self.get_rect().colliderect(other_obj.get_rect())