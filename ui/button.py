"""
Balatro-styled rounded action button component.
"""
import pygame
from ui.ui_element import UIElement
from settings import C


class Button(UIElement):
    def __init__(self, x: int, y: int, w: int, h: int, text: str,
                 bg_color=C.BTN_BLUE, hover_color=C.BTN_BLUE_HI,
                 text_color=C.WHITE, font_size=24, callback=None):
        super().__init__(x, y, w, h)
        self.text = text
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size = font_size
        self.callback = callback

    def on_click(self) -> bool:
        if self.callback:
            self.callback()
            return True
        return False

    def draw(self, surface: pygame.Surface, font):
        if not self.visible:
            return

        col = self.hover_color if (self.is_hovered and self.enabled) else self.bg_color
        if not self.enabled:
            col = C.BTN_DISABLED

        sw = int(self.rect.width * self.scale)
        sh = int(self.rect.height * self.scale)
        cx, cy = self.rect.center

        btn_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        
        # Shadow
        pygame.draw.rect(btn_surf, (0, 0, 0, 80), (0, 4, self.rect.width, self.rect.height - 4), border_radius=8)
        # Main fill
        pygame.draw.rect(btn_surf, col, (0, 0, self.rect.width, self.rect.height - 4), border_radius=8)
        # Inner highlight border
        pygame.draw.rect(btn_surf, (255, 255, 255, 40), (0, 0, self.rect.width, self.rect.height - 4), width=2, border_radius=8)

        # Render text
        txt_sf = font.render(self.text, True, self.text_color)
        txt_rect = txt_sf.get_rect(center=(self.rect.width // 2, (self.rect.height - 4) // 2))
        btn_surf.blit(txt_sf, txt_rect)

        if self.scale != 1.0:
            btn_surf = pygame.transform.smoothscale(btn_surf, (sw, sh))

        draw_rect = btn_surf.get_rect(center=(cx, cy))
        surface.blit(btn_surf, draw_rect)
