import pygame
from objects.game_object import GameObject
from objects.bullet import Bullet

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
        self.direction = 0

        # Свойства для бонуса двойного выстрела
        self.double_shot_active = False
        self.double_shot_end_time = 0
        self.double_shot_cooldown = getattr(config, 'double_shot_cooldown', 100)

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

    def activate_double_shot(self, duration):
        """Активирует бонус двойного выстрела"""
        self.double_shot_active = True
        self.double_shot_end_time = pygame.time.get_ticks() + duration * 1000
        print(f"Двойной выстрел активирован на {duration} секунд!")

    def update(self, dt):
        """Обновляет позицию игрока и проверяет бонусы"""
        self.x += self.direction * self.speed * dt

        # Ограничение движения в пределах экрана
        if self.x < 0:
            self.x = 0
        elif self.x > self.config.window_width - self.width:
            self.x = self.config.window_width - self.width

        # Проверка окончания бонуса двойного выстрела
        if self.double_shot_active and pygame.time.get_ticks() > self.double_shot_end_time:
            self.double_shot_active = False
            print("Бонус двойного выстрела закончился!")

    def shoot(self):
        """Создает пули - обычные или двойные в зависимости от бонуса"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.double_shot_cooldown:
            self.last_shot_time = current_time

            if self.double_shot_active:
                # Двойной выстрел по диагоналям
                return self._create_double_shot()
            else:
                # Обычный одиночный выстрел
                bullet_x = self.x + self.width // 2 - 2
                bullet_y = self.y
                return [Bullet(bullet_x, bullet_y, -self.config.bullet_speed, True)]
        return []

    def _create_double_shot(self):
        """Создает две пули, летящие по диагоналям"""
        bullets = []

        # Левая диагональная пуля (немного левее и под углом)
        left_bullet_x = self.x + self.width // 4 - 2
        left_bullet_y = self.y
        bullets.append(Bullet(left_bullet_x, left_bullet_y, -self.config.bullet_speed, True, -1))

        # Правая диагональная пуля (немного правее и под углом)
        right_bullet_x = self.x + 3 * self.width // 4 - 2
        right_bullet_y = self.y
        bullets.append(Bullet(right_bullet_x, right_bullet_y, -self.config.bullet_speed, True, 1))

        return bullets

    def draw(self, surface, color):
        """Отрисовывает игрока с индикацией бонуса"""
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(surface, color, points)

        # Индикация активного бонуса двойного выстрела
        if self.double_shot_active:
            # Рисуем сияние вокруг корабля
            glow_color = (0, 255, 255)
            pygame.draw.polygon(surface, glow_color, points, 2)