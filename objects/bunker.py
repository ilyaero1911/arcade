import pygame
from objects.game_object import GameObject

import pygame
from objects.game_object import GameObject


class Bunker(GameObject):
    """Улучшенный класс бункера с постепенным разрушением"""

    def __init__(self, x, y, config):
        super().__init__(x, y, config.bunker_width, config.bunker_height)
        self.config = config
        # Создаем маску для постепенного разрушения (8x6 блоков)
        self.blocks = [[True for _ in range(6)] for _ in range(8)]
        self.block_width = self.width // 6
        self.block_height = self.height // 8

    def take_damage(self, bullet_x, bullet_y):
        """Разрушает блоки бункера в месте попадания"""
        # Определяем, в какой блок попала пуля
        local_x = int((bullet_x - self.x) / self.block_width)
        local_y = int((bullet_y - self.y) / self.block_height)

        # Уничтожаем блок и соседние (для большего разрушения)
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                ny, nx = local_y + dy, local_x + dx
                if 0 <= ny < len(self.blocks) and 0 <= nx < len(self.blocks[0]):
                    self.blocks[ny][nx] = False

    def is_colliding_with(self, other_obj):
        """Проверяет столкновение с неповрежденными блоками"""
        other_rect = other_obj.get_rect()

        for y, row in enumerate(self.blocks):
            for x, block in enumerate(row):
                if block:
                    block_rect = pygame.Rect(
                        self.x + x * self.block_width,
                        self.y + y * self.block_height,
                        self.block_width, self.block_height
                    )
                    if block_rect.colliderect(other_rect):
                        # Если есть столкновение, наносим урон бункеру
                        if hasattr(other_obj, 'x') and hasattr(other_obj, 'y'):
                            self.take_damage(other_obj.x, other_obj.y)
                        return True
        return False

    def draw(self, surface, color):
        """Отрисовывает только неповрежденные блоки"""
        for y, row in enumerate(self.blocks):
            for x, block in enumerate(row):
                if block:
                    block_x = self.x + x * self.block_width
                    block_y = self.y + y * self.block_height
                    pygame.draw.rect(surface, color,
                                     (block_x, block_y,
                                      self.block_width, self.block_height))