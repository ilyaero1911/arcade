import json
import os
import pygame


class GameConfig:
    """Класс для загрузки и хранения конфигурации игры"""

    def __init__(self):
        self.load_config()

    def load_config(self):
        """Загружает конфигурацию из JSON файлов"""
        try:
            # Загрузка игровой конфигурации
            with open('config/game_config.json', 'r') as f:
                game_config = json.load(f)

            # Загрузка графической конфигурации
            with open('config/graphics.json', 'r') as f:
                graphics_config = json.load(f)

            # Основные настройки игры
            self.title = game_config["game"]["title"]
            self.version = game_config["game"]["version"]
            self.window_width = game_config["game"]["window_width"]
            self.window_height = game_config["game"]["window_height"]
            self.initial_lives = game_config["game"]["initial_lives"]

            # Настройки игрока
            player_config = game_config["player"]
            self.player_width = player_config["width"]
            self.player_height = player_config["height"]
            self.player_speed = player_config["speed"]
            self.bullet_speed = player_config["bullet_speed"]
            self.bullet_cooldown = player_config["bullet_cooldown"]

            # Настройки пришельцев
            invaders_config = game_config["invaders"]
            self.invader_rows = invaders_config["rows"]
            self.invader_cols = invaders_config["cols"]
            self.invader_width = invaders_config["width"]
            self.invader_height = invaders_config["height"]
            self.invader_horizontal_speed = invaders_config["horizontal_speed"]
            self.invader_vertical_speed = invaders_config["vertical_speed"]
            self.invader_bullet_speed = invaders_config["bullet_speed"]
            self.invader_bullet_chance = invaders_config["bullet_chance"]
            self.invader_points = invaders_config["points"]

            # Настройки таинственного корабля
            mystery_config = game_config["mystery_ship"]
            self.mystery_width = mystery_config["width"]
            self.mystery_height = mystery_config["height"]
            self.mystery_speed = mystery_config["speed"]
            self.mystery_spawn_chance = mystery_config["spawn_chance"]
            self.mystery_points = mystery_config["points"]

            # Настройки укрытий
            bunkers_config = game_config["bunkers"]
            self.bunker_count = bunkers_config["count"]
            self.bunker_width = bunkers_config["width"]
            self.bunker_height = bunkers_config["height"]

            # Графические настройки
            self.colors = graphics_config["colors"]
            self.ui_config = graphics_config["ui"]

        except Exception as e:
            print(f"Error loading config: {e}")
            # Значения по умолчанию
            self.set_defaults()

    def set_defaults(self):
        """Устанавливает значения по умолчанию при ошибке загрузки конфигурации"""
        self.window_width = 800
        self.window_height = 600
        self.initial_lives = 3
        self.player_width = 50
        self.player_height = 30
        self.player_speed = 300
        self.double_shot_duration = 10  # 10 секунд
        self.double_shot_cooldown = 100  # ms между выстрелами в режиме двойного