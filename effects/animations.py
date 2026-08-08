"""
Animation & easing utilities.
"""
import math


def ease_out_cubic(t):
    return 1 - (1 - t) ** 3

def ease_in_cubic(t):
    return t ** 3

def ease_in_out_cubic(t):
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - (-2 * t + 2) ** 3 / 2

def ease_out_bounce(t):
    n1, d1 = 7.5625, 2.75
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375

def ease_out_elastic(t):
    if t == 0 or t == 1:
        return t
    return 2 ** (-10 * t) * math.sin((t * 10 - 0.75) * (2 * math.pi / 3)) + 1

def ease_out_back(t):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))


class Tween:
    """Animates a single float value from start to end over duration."""

    def __init__(self, start, end, duration, ease_fn=ease_out_cubic,
                 delay=0.0, on_complete=None):
        self.start = start
        self.end = end
        self.duration = max(duration, 0.001)
        self.ease_fn = ease_fn
        self.delay = delay
        self.on_complete = on_complete
        self._elapsed = 0.0
        self.value = start
        self.done = False

    def update(self, dt):
        if self.done:
            return self.value
        self._elapsed += dt
        if self._elapsed < self.delay:
            self.value = self.start
            return self.value
        t = min((self._elapsed - self.delay) / self.duration, 1.0)
        self.value = lerp(self.start, self.end, self.ease_fn(t))
        if t >= 1.0:
            self.done = True
            self.value = self.end
            if self.on_complete:
                self.on_complete()
        return self.value

    def reset(self):
        self._elapsed = 0.0
        self.value = self.start
        self.done = False


class TweenSequence:
    """Runs a list of Tweens one after another."""

    def __init__(self, tweens: list):
        self.tweens = tweens
        self._index = 0
        self.done = False
        self.value = tweens[0].start if tweens else 0

    def update(self, dt):
        if self.done or not self.tweens:
            return self.value
        tw = self.tweens[self._index]
        self.value = tw.update(dt)
        if tw.done:
            self._index += 1
            if self._index >= len(self.tweens):
                self.done = True
        return self.value
