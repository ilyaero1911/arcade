import pygame
from config.game_config import GameConfig


class Renderer:
    """Класс для отрисовки всех игровых объектов"""

    def __init__(self, config: GameConfig):
        self.config = config
        self.screen = pygame.display.set_mode((config.window_width, config.window_height))
        pygame.display.set_caption(f"{config.title} v{config.version}")

        # Загрузка шрифтов
        self.font = pygame.font.Font(None, config.ui_config["font_size"])
        self.title_font = pygame.font.Font(None, config.ui_config["title_font_size"])

        # Цвета
        self.colors = config.colors

    def render(self, engine):
        """Отрисовывает весь игровой экран"""
        # Очистка экрана
        self.screen.fill(self.colors["background"])

        if engine.game_state == "menu":
            self.render_menu()
        elif engine.game_state == "playing" or engine.game_state == "paused":
            self.render_game(engine)
            if engine.game_state == "paused":
                self.render_pause_screen()
        elif engine.game_state == "game_over":
            self.render_game(engine)
            self.render_game_over_screen(engine)

        # Обновление HUD
        self.render_hud(engine)

    def render_menu(self):
        """Отрисовывает главное меню"""
        title = self.title_font.render("SPACE INVADERS", True, self.colors["text"])
        instruction = self.font.render("Press SPACE to start", True, self.colors["text"])

        title_rect = title.get_rect(center=(self.config.window_width // 2, self.config.window_height // 3))
        instruction_rect = instruction.get_rect(center=(self.config.window_width // 2, self.config.window_height // 2))

        self.screen.blit(title, title_rect)
        self.screen.blit(instruction, instruction_rect)

    def render_game(self, engine):
        """Отрисовывает игровые объекты"""
        # Отрисовка игрока
        engine.player.draw(self.screen, self.colors["player"])

        # Отрисовка пришельцев
        for invader in engine.invaders:
            color_key = f"invader{(invader.type % 5) + 1}"
            color = self.colors.get(color_key, self.colors["invader1"])
            invader.draw(self.screen, color)

            # Отрисовка пуль с разными цветами
        for bullet in engine.bullets:
            if bullet.is_player_bullet:
                color = self.colors["bullet_player"]  # СИНИЙ для игрока
            else:
                color = self.colors["bullet_invader"]  # ЗЕЛЕНЫЙ для пришельцев
            bullet.draw(self.screen, color)

        # Отрисовка таинственного корабля
        if engine.mystery_ship:
            engine.mystery_ship.draw(self.screen, self.colors["mystery_ship"])

        # Отрисовка укрытий
        for bunker in engine.bunkers:
            bunker.draw(self.screen, self.colors["bunker"])  # БЕЛЫЙ

    def render_hud(self, engine):
        """Отрисовывает интерфейс с информацией о бонусе"""
        # Счет
        score_text = self.font.render(f"Score: {engine.score}", True, self.colors["text"])
        self.screen.blit(score_text, (10, 10))

        # Рекорд
        high_score_text = self.font.render(f"High Score: {engine.high_score}", True, self.colors["text"])
        self.screen.blit(high_score_text, (self.config.window_width - 200, 10))

        # Жизни
        lives_text = self.font.render(f"Lives: {engine.player.lives}", True, self.colors["text"])
        self.screen.blit(lives_text, (10, self.config.window_height - 40))

        # Индикатор бонуса двойного выстрела
        if engine.player.double_shot_active:
            time_left = (engine.player.double_shot_end_time - pygame.time.get_ticks()) // 1000
            bonus_text = self.font.render(f"Double Shot: {time_left}s", True, (0, 255, 255))
            bonus_rect = bonus_text.get_rect(center=(self.config.window_width // 2, 30))
            self.screen.blit(bonus_text, bonus_rect)



    def render_pause_screen(self):
        """Отрисовывает экран паузы"""
        overlay = pygame.Surface((self.config.window_width, self.config.window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        pause_text = self.title_font.render("PAUSED", True, self.colors["text"])
        pause_rect = pause_text.get_rect(center=(self.config.window_width // 2, self.config.window_height // 2))
        self.screen.blit(pause_text, pause_rect)

    def render_game_over_screen(self, engine):
        """Отрисовывает экран окончания игры"""
        overlay = pygame.Surface((self.config.window_width, self.config.window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.title_font.render("GAME OVER", True, self.colors["text"])
        score_text = self.font.render(f"Final Score: {engine.score}", True, self.colors["text"])
        restart_text = self.font.render("Press R to restart", True, self.colors["text"])

        game_over_rect = game_over_text.get_rect(center=(self.config.window_width // 2, self.config.window_height // 3))
        score_rect = score_text.get_rect(center=(self.config.window_width // 2, self.config.window_height // 2))
        restart_rect = restart_text.get_rect(center=(self.config.window_width // 2, self.config.window_height // 1.5))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)