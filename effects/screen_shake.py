"""
Screen shake effect.
"""
import random
import math


class ScreenShake:
    """Call trigger() to start a shake; offset() returns current displacement."""

    def __init__(self):
        self._intensity = 0.0
        self._duration = 0.0
        self._elapsed = 0.0
        self._ox = 0.0
        self._oy = 0.0
        self._freq = 30.0

    def trigger(self, intensity=6.0, duration=0.3):
        self._intensity = intensity
        self._duration = duration
        self._elapsed = 0.0

    def update(self, dt):
        if self._elapsed >= self._duration:
            self._ox = self._oy = 0.0
            return
        self._elapsed += dt
        t = 1.0 - min(self._elapsed / self._duration, 1.0)  # decay
        amp = self._intensity * t
        phase = self._elapsed * self._freq
        self._ox = amp * math.sin(phase * 1.1 + random.random() * 0.5)
        self._oy = amp * math.cos(phase * 0.9 + random.random() * 0.5)

    def offset(self):
        return int(self._ox), int(self._oy)

    @property
    def active(self):
        return self._elapsed < self._duration
