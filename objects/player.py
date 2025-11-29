import pygame
from objects.game_object import GameObject
from objects.bullet import Bullet


class Player(GameObject):
    """Класс игрока"""

    def __init__(self, x, y, config):
        super().__init__(x, y, config.player_width, config.player_height)
        self.config = config
        self.lives = config.initial_lives
        self.score = 0
        self.speed = config.player_speed
        self.last_shot_time = 0
        self.direction = 0  # -1: left, 0: stop, 1: right

    def handle_event(self, event):
        """Обрабатывает события ввода"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.direction = -1
            elif event.key == pygame.K_RIGHT:
                self.direction = 1
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.direction = 0

    def update(self, dt):
        """Обновляет позицию игрока"""
        self.x += self.direction * self.speed * dt

        # Ограничение движения в пределах экрана
        if self.x < 0:
            self.x = 0
        elif self.x > self.config.window_width - self.width:
            self.x = self.config.window_width - self.width

    def shoot(self):
        """Создает пулю"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.config.bullet_cooldown:
            self.last_shot_time = current_time
            bullet_x = self.x + self.width // 2 - 2
            bullet_y = self.y
            return Bullet(bullet_x, bullet_y, -self.config.bullet_speed, True)
        return None

    def draw(self, surface, color):
        """Отрисовывает игрока в виде треугольника"""
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(surface, color, points)