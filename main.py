"""
Poker2 – Main Entry Point
Integración del diseño avanzado de example/ con la lógica de juego de poker_clon/.
"""
import pygame
from settings import DESIGN_W, DESIGN_H, FPS, C
from assets import AssetManager
from core.game_state import GameState
from engine.sound_manager import SoundManager
from effects.background import VortexBackground
from effects.crt_shader import CRTFilter

from screens.screen_manager import ScreenManager
from screens.title_screen import TitleScreen
from screens.main_menu import MainMenuScreen
from screens.blind_select import BlindSelectScreen
from screens.gameplay_screen import GameplayScreen
from screens.shop_screen import ShopScreen
from screens.game_over import GameOverScreen
from screens.collection_screen import CollectionScreen
from screens.settings_screen import SettingsScreen
from screens.debug_screen import DebugScreen
from screens.win_screen import WinScreen


def main():
    pygame.init()
    if hasattr(pygame, 'mixer'):
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
        except Exception:
            pass

    screen = pygame.display.set_mode((DESIGN_W, DESIGN_H), pygame.RESIZABLE | pygame.SCALED)
    pygame.display.set_caption("Poker2 – Balatro Clone")
    clock = pygame.time.Clock()

    # Core Systems
    assets = AssetManager()
    assets.load()

    state = GameState()
    sound = SoundManager()
    bg = VortexBackground()
    crt = CRTFilter()

    # Screen Manager
    sm = ScreenManager()

    # Register all screens
    sm.register("title", TitleScreen(sm, state))
    sm.register("main_menu", MainMenuScreen(sm, state))
    sm.register("blind_select", BlindSelectScreen(sm, state))
    sm.register("gameplay", GameplayScreen(sm, state, sound))
    sm.register("shop", ShopScreen(sm, state, sound))
    sm.register("game_over", GameOverScreen(sm, state, sound))
    sm.register("win", WinScreen(sm, state))
    sm.register("collection", CollectionScreen(sm, state))
    sm.register("settings", SettingsScreen(sm, state, crt, sound))
    sm.register("debug", DebugScreen(sm, state))

    sm.change_screen("title")

    # Start music
    try:
        sound.play_music("lobby")
    except Exception:
        pass

    render_surface = pygame.Surface((DESIGN_W, DESIGN_H))
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        dt = min(dt, 0.05)  # Cap delta time

        # Scaled mouse position
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F1:
                    sm.change_screen("debug")
            sm.handle_event(event)

        # Update
        bg.update(dt)
        crt.update(dt)
        sound.update(dt)
        sm.update(dt, mouse_pos)

        # Draw
        render_surface.fill(C.BG_DARK)
        bg.draw(render_surface)

        sm.draw(render_surface, assets)

        crt.apply(render_surface)

        screen.blit(render_surface, (0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
