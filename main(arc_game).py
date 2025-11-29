import pygame
import sys

# Импорт наших модулей
from config.game_config import GameConfig
from engine.game_engine import GameEngine
from engine.renderer import Renderer


def main():
    """Основная функция игры"""
    try:
        # Инициализация pygame
        pygame.init()

        # Загрузка конфигурации
        config = GameConfig()

        # Создание движка и рендерера
        engine = GameEngine(config)
        renderer = Renderer(config)

        # Основной игровой цикл
        clock = pygame.time.Clock()
        running = True

        while running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if engine.game_state == "playing":
                            engine.game_state = "paused"
                        elif engine.game_state == "paused":
                            engine.game_state = "playing"
                    elif event.key == pygame.K_r and engine.game_state == "game_over":
                        engine.reset_game()
                    elif event.key == pygame.K_SPACE:
                        if engine.game_state == "menu":
                            engine.game_state = "playing"
                        elif engine.game_state == "playing":
                            engine.player_shoot()

                engine.handle_event(event)

            # Обновление состояния игры
            dt = clock.tick(60) / 1000.0  # Дельта времени в секундах
            engine.update(dt)

            # Отрисовка
            renderer.render(engine)

            # Обновление экрана
            pygame.display.flip()

        # Завершение работы
        pygame.quit()
        sys.exit()

    except Exception as e:
        print(f"Error in main: {e}")
        pygame.quit()
        sys.exit(1)

main()