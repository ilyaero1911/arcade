import pygame
import random
from config.game_config import GameConfig
from objects.player import Player
from objects.invader import Invader
from objects.mystery_ship import MysteryShip
from objects.bunker import Bunker


class GameEngine:
    """Основной движок игры, управляющий всей логикой"""

    def __init__(self, config: GameConfig):
        self.config = config
        self.game_state = "menu"  # menu, playing, paused, game_over
        self.score = 0
        self.high_score = 0

        # Инициализация игровых объектов
        self.player = None
        self.invaders = []
        self.bullets = []
        self.mystery_ship = None
        self.bunkers = []

        self.reset_game()

    def reset_game(self):
        """Сбрасывает игру в начальное состояние"""
        self.score = 0
        self.game_state = "playing"

        # Создание игрока
        player_x = self.config.window_width // 2 - self.config.player_width // 2
        player_y = self.config.window_height - 100
        self.player = Player(player_x, player_y, self.config)

        # Создание пришельцев
        self.create_invaders()

        # Создание укрытий
        self.create_bunkers()

        # Очистка пуль и таинственного корабля
        self.bullets = []
        self.mystery_ship = None

    def create_invaders(self):
        """Создает сетку пришельцев"""
        self.invaders = []
        start_x = 50
        start_y = 50
        spacing = 10

        for row in range(self.config.invader_rows):
            for col in range(self.config.invader_cols):
                x = start_x + col * (self.config.invader_width + spacing)
                y = start_y + row * (self.config.invader_height + spacing)
                points = self.config.invader_points[row % len(self.config.invader_points)]
                invader = Invader(x, y, row, self.config, points)
                self.invaders.append(invader)

    def create_bunkers(self):
        """Создает укрытия"""
        self.bunkers = []
        spacing = self.config.window_width // (self.config.bunker_count + 1)

        for i in range(self.config.bunker_count):
            x = spacing * (i + 1) - self.config.bunker_width // 2
            y = self.config.window_height - 200
            bunker = Bunker(x, y, self.config)
            self.bunkers.append(bunker)

    def handle_event(self, event):
        """Обрабатывает события ввода"""
        if self.game_state == "playing":
            self.player.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player_shoot()

    def update(self, dt):
        """Обновляет состояние игры"""
        if self.game_state != "playing":
            return

        # Обновление игрока
        self.player.update(dt)

        # ОБНОВЛЕННАЯ ЛОГИКА ДВИЖЕНИЯ ПРИШЕЛЬЦЕВ
        should_move_down = False
        should_change_direction = False

        # Проверяем, достигли ли пришельцы края экрана
        if self.invaders:
            # Проверяем по первому пришельцу (можно оптимизировать)
            sample_invader = self.invaders[0]
            if sample_invader.should_move_down(self.invaders):
                should_move_down = True
                should_change_direction = True

        # Обновление пришельцев
        for invader in self.invaders:
            invader.update(dt)

            # Если нужно спуститься - спускаем всех пришельцев
            if should_move_down and not invader.has_moved_down:
                invader.move_down()

            # Если нужно сменить направление - меняем у всех
            if should_change_direction:
                invader.change_direction()

        # Обновление пуль
        for bullet in self.bullets[:]:
            bullet.update(dt)

            # Удаление пуль за пределами экрана
            if (bullet.y < 0 or bullet.y > self.config.window_height or
                    bullet.x < 0 or bullet.x > self.config.window_width):
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
                continue

            # Проверка столкновений с бункерами
            for bunker in self.bunkers[:]:
                if bunker.is_colliding_with(bullet):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break

            if bullet not in self.bullets:
                continue

            # Проверка столкновений с таинственным кораблем
            if bullet.is_player_bullet and self.mystery_ship:
                if self.mystery_ship.is_colliding_with(bullet):
                    # Начисление очков за попадание
                    self.score += self.config.mystery_points

                    # АКТИВАЦИЯ БОНУСА ДВОЙНОГО ВЫСТРЕЛА
                    duration = getattr(self.config, 'double_shot_duration', 10)
                    self.player.activate_double_shot(duration)

                    print(f"Таинственный корабль уничтожен! +{self.config.mystery_points} очков")
                    print(f"Бонус: двойной выстрел на {duration} секунд!")

                    self.mystery_ship = None
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    continue

            # Проверка столкновений пуль с пришельцами
            if bullet.is_player_bullet:
                for invader in self.invaders[:]:
                    if invader.is_colliding_with(bullet):
                        self.score += invader.points
                        self.invaders.remove(invader)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        break
            else:
                # Столкновение пуль пришельцев с игроком
                if self.player.is_colliding_with(bullet):
                    self.player.lives -= 1
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if self.player.lives <= 0:
                        self.game_state = "game_over"
                        self.high_score = max(self.high_score, self.score)

        if self.mystery_ship:
            self.mystery_ship.update(dt)
            if self.mystery_ship.x > self.config.window_width:
                self.mystery_ship = None
        else:
            if random.random() < self.config.mystery_spawn_chance:
                self.mystery_ship = MysteryShip(self.config)

            # Пришельцы стреляют
        for invader in self.invaders:
            if random.random() < self.config.invader_bullet_chance:
                bullet = invader.shoot()
                if bullet:
                    self.bullets.append(bullet)

            # Проверка условий победы/поражения
        if not self.invaders:
            self.create_invaders()

        for invader in self.invaders:
            if invader.y + invader.height > self.player.y:
                self.game_state = "game_over"
                self.high_score = max(self.high_score, self.score)
                break

    def player_shoot(self):
        """Создает пули от игрока с учетом бонусов"""
        if self.game_state == "playing":
            bullets = self.player.shoot()
            for bullet in bullets:
                self.bullets.append(bullet)