"""
Particle system for scoring effects, sparkles, and floating score popups.
"""
import random
import math
import pygame


class Particle:
    __slots__ = ('x', 'y', 'vx', 'vy', 'life', 'max_life',
                 'color', 'size', 'gravity', 'alpha_decay')

    def __init__(self, x, y, vx, vy, life, color, size=3,
                 gravity=0, alpha_decay=True):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = size
        self.gravity = gravity
        self.alpha_decay = alpha_decay


class ScorePopupText:
    """Floating popup text (e.g. '+10 Chips', '+4 Mult', 'X1.5') over cards."""

    def __init__(self, text: str, x: float, y: float, color: tuple, duration=0.8):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.duration = duration
        self.elapsed = 0.0
        self.done = False

    def update(self, dt: float):
        self.elapsed += dt
        self.y -= dt * 45.0  # float upward
        if self.elapsed >= self.duration:
            self.done = True

    def draw(self, surface: pygame.Surface, font):
        if self.done:
            return
        t = 1.0 - min(self.elapsed / self.duration, 1.0)
        alpha = int(255 * min(t * 2.0, 1.0))
        
        txt_sf = font.render(self.text, True, self.color)
        txt_sh = font.render(self.text, True, (0, 0, 0))
        
        txt_sf.set_alpha(alpha)
        txt_sh.set_alpha(alpha)

        surface.blit(txt_sh, (self.x + 2 - txt_sf.get_width() // 2, self.y + 2 - txt_sf.get_height() // 2))
        surface.blit(txt_sf, (self.x - txt_sf.get_width() // 2, self.y - txt_sf.get_height() // 2))


class ParticleSystem:
    def __init__(self, max_particles=300):
        self.particles: list[Particle] = []
        self.popups: list[ScorePopupText] = []
        self.max_particles = max_particles

    def emit_popup(self, text: str, x: float, y: float, color: tuple):
        self.popups.append(ScorePopupText(text, x, y, color))

    def emit(self, x, y, color, count=10, speed=80, life=0.8,
             spread=math.pi * 2, angle=0, size=3, gravity=120):
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                break
            a = angle + random.uniform(-spread / 2, spread / 2)
            s = random.uniform(speed * 0.3, speed)
            l = random.uniform(life * 0.5, life)
            sz = random.uniform(size * 0.5, size * 1.5)
            p = Particle(x, y, s * math.cos(a), s * math.sin(a),
                         l, color, sz, gravity)
            self.particles.append(p)

    def emit_burst(self, x, y, colors, count=25, speed=120,
                   life=0.6, size=4):
        """Radial burst used for scoring."""
        for i in range(count):
            if len(self.particles) >= self.max_particles:
                break
            a = (i / count) * math.pi * 2 + random.uniform(-0.2, 0.2)
            s = random.uniform(speed * 0.4, speed)
            col = random.choice(colors)
            l = random.uniform(life * 0.5, life)
            p = Particle(x, y, s * math.cos(a), s * math.sin(a),
                         l, col, random.uniform(2, size), gravity=60)
            self.particles.append(p)

    def update(self, dt):
        alive = []
        for p in self.particles:
            p.life -= dt
            if p.life <= 0:
                continue
            p.vy += p.gravity * dt
            p.x += p.vx * dt
            p.y += p.vy * dt
            p.vx *= 0.98
            alive.append(p)
        self.particles = alive

        alive_popups = []
        for pop in self.popups:
            pop.update(dt)
            if not pop.done:
                alive_popups.append(pop)
        self.popups = alive_popups

    def draw(self, surface, font=None):
        for p in self.particles:
            t = max(p.life / p.max_life, 0)
            alpha = int(255 * t) if p.alpha_decay else 255
            sz = max(1, int(p.size * t))
            if alpha < 10:
                continue
            col = (*p.color[:3], alpha)
            s = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, col, (sz, sz), sz)
            surface.blit(s, (int(p.x) - sz, int(p.y) - sz))

        if font:
            for pop in self.popups:
                pop.draw(surface, font)

    def clear(self):
        self.particles.clear()
        self.popups.clear()
