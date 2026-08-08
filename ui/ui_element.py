"""
Base class for UI interactive elements with hover, click, scale, and animation handling.
"""
import pygame


class UIElement:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.rect = pygame.Rect(x, y, w, h)
        self.is_hovered = False
        self.is_pressed = False
        self.scale = 1.0
        self.target_scale = 1.0
        self.visible = True
        self.enabled = True

    def get_hit_rect(self) -> pygame.Rect:
        return self.rect

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        if not self.visible:
            return
        
        hit_rect = self.get_hit_rect()
        self.is_hovered = hit_rect.collidepoint(mouse_pos) and self.enabled
        self.target_scale = 1.05 if self.is_hovered else 1.0
        # Smooth interpolation for scale
        self.scale += (self.target_scale - self.scale) * min(dt * 15.0, 1.0)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible or not self.enabled:
            return False

        hit_rect = self.get_hit_rect()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hit_rect.collidepoint(event.pos):
                self.is_pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed:
                self.is_pressed = False
                if hit_rect.collidepoint(event.pos):
                    return self.on_click()
        return False

    def on_click(self) -> bool:
        return True

    def draw(self, surface: pygame.Surface):
        pass
