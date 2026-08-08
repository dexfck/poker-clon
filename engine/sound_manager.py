"""
Sistema de audio del juego.
- Música sincronizada: ingame y shop suenan simultáneamente,
  se controlan con volúmenes de canal para crossfade perfecto.
- SFX contextuales con variación aleatoria.
"""
import os
import random
from typing import Dict, List, Optional
import pygame
from settings import MUSIC_VOLUME, SFX_VOLUME, SOUND_DIR


class SoundManager:
    """Administrador de audio y música con soporte de crossfade sincronizado."""

    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
        pygame.mixer.set_num_channels(16)

        self.music_volume = MUSIC_VOLUME
        self.sfx_volume = SFX_VOLUME

        # Precargar SFX
        self.sfx_chips: List[pygame.mixer.Sound] = []
        self.sfx_mult: List[pygame.mixer.Sound] = []
        self.sfx_coins: List[pygame.mixer.Sound] = []
        self.sfx_win: Optional[pygame.mixer.Sound] = None

        try:
            self.sfx_chips = [
                pygame.mixer.Sound(os.path.join(SOUND_DIR, "chips1.ogg")),
                pygame.mixer.Sound(os.path.join(SOUND_DIR, "chips2.ogg")),
            ]
        except Exception:
            pass

        try:
            self.sfx_mult = []
            for fname in ["multhit1.ogg", "multhit2.ogg", "multi1.ogg", "multi2.ogg"]:
                for folder in [SOUND_DIR, os.path.join("assets", "sound"), os.path.join("resources", "sounds")]:
                    p = os.path.join(folder, fname)
                    if os.path.exists(p):
                        try:
                            s = pygame.mixer.Sound(p)
                            if s not in self.sfx_mult:
                                self.sfx_mult.append(s)
                        except Exception:
                            pass
        except Exception:
            pass

        try:
            self.sfx_coins = [
                pygame.mixer.Sound(os.path.join(SOUND_DIR, f"coin{i}.ogg"))
                for i in range(2, 8)
            ]
        except Exception:
            pass

        try:
            self.sfx_win = pygame.mixer.Sound(
                os.path.join(SOUND_DIR, "win.ogg")
            )
        except Exception:
            pass

        try:
            p_whoosh = os.path.join("resources", "sounds", "whoosh_long.ogg")
            if os.path.exists(p_whoosh):
                self.sfx_whoosh_long = pygame.mixer.Sound(p_whoosh)
            else:
                self.sfx_whoosh_long = None
        except Exception:
            self.sfx_whoosh_long = None

        for snd in self.sfx_chips + self.sfx_mult + self.sfx_coins:
            snd.set_volume(self.sfx_volume)
        if self.sfx_win:
            self.sfx_win.set_volume(self.sfx_volume)
        if self.sfx_whoosh_long:
            self.sfx_whoosh_long.set_volume(self.sfx_volume)

        # Pistas musicales
        processed_dir = os.path.join(SOUND_DIR, "processed")
        self.music_tracks: Dict[str, pygame.mixer.Sound] = {}
        for key in ["lobby", "ingame", "shop"]:
            path = os.path.join(processed_dir, f"music_{key}.ogg")
            if os.path.exists(path):
                try:
                    self.music_tracks[key] = pygame.mixer.Sound(path)
                except Exception:
                    pass

        # Load music3.ogg for defeat screen
        p_music3 = os.path.join("resources", "sounds", "music3.ogg")
        if os.path.exists(p_music3):
            try:
                self.music_tracks["defeat"] = pygame.mixer.Sound(p_music3)
            except Exception:
                pass

        for track in self.music_tracks.values():
            track.set_volume(self.music_volume)

        # Canales dedicados para reproducción sincronizada
        self.ch_lobby = pygame.mixer.Channel(0)
        self.ch_ingame = pygame.mixer.Channel(1)
        self.ch_shop = pygame.mixer.Channel(2)
        self.ch_defeat = pygame.mixer.Channel(3)

        # Estado
        self.current_music_key: Optional[str] = None
        self.music_playing: bool = False
        self.music_muted: bool = False

        # Estado de Crossfade
        self.crossfade_active: bool = False
        self.crossfade_duration: float = 1.0
        self.crossfade_timer: float = 0.0
        self.crossfade_from_channel: Optional[pygame.mixer.Channel] = None
        self.crossfade_to_channel: Optional[pygame.mixer.Channel] = None

    def toggle_mute_music(self) -> bool:
        """Alterna el estado de silencio de la música."""
        self.music_muted = not self.music_muted
        if self.music_muted:
            self.ch_lobby.set_volume(0.0)
            self.ch_ingame.set_volume(0.0)
            self.ch_shop.set_volume(0.0)
            if self.ch_defeat:
                self.ch_defeat.set_volume(0.0)
        else:
            if self.current_music_key == "lobby":
                self.ch_lobby.set_volume(1.0)
            elif self.current_music_key == "ingame":
                self.ch_ingame.set_volume(1.0)
                self.ch_shop.set_volume(0.0)
                if self.ch_defeat:
                    self.ch_defeat.set_volume(0.0)
            elif self.current_music_key == "shop":
                self.ch_ingame.set_volume(0.0)
                self.ch_shop.set_volume(1.0)
                if self.ch_defeat:
                    self.ch_defeat.set_volume(0.0)
            elif self.current_music_key == "defeat":
                self.ch_ingame.set_volume(0.0)
                self.ch_shop.set_volume(0.0)
                if self.ch_defeat:
                    self.ch_defeat.set_volume(1.0)
        return self.music_muted

    def play_music(self, key: str) -> None:
        """Inicia una pista musical desde el principio."""
        if key not in self.music_tracks:
            return

        self._stop_all_music()
        self.crossfade_active = False

        if key == "lobby":
            self.ch_lobby.set_volume(0.0 if self.music_muted else 1.0)
            self.ch_lobby.play(self.music_tracks["lobby"], loops=-1)
        elif key == "ingame":
            self.ch_ingame.set_volume(0.0 if self.music_muted else 1.0)
            self.ch_shop.set_volume(0.0)
            if self.ch_defeat:
                self.ch_defeat.set_volume(0.0)
            self.ch_ingame.play(self.music_tracks["ingame"], loops=-1)
            if "shop" in self.music_tracks:
                self.ch_shop.play(self.music_tracks["shop"], loops=-1)
            if "defeat" in self.music_tracks and self.ch_defeat:
                self.ch_defeat.play(self.music_tracks["defeat"], loops=-1)
        elif key == "shop":
            self.ch_ingame.set_volume(0.0)
            self.ch_shop.set_volume(0.0 if self.music_muted else 1.0)
            if self.ch_defeat:
                self.ch_defeat.set_volume(0.0)
            if "ingame" in self.music_tracks:
                self.ch_ingame.play(self.music_tracks["ingame"], loops=-1)
            self.ch_shop.play(self.music_tracks["shop"], loops=-1)
            if "defeat" in self.music_tracks and self.ch_defeat:
                self.ch_defeat.play(self.music_tracks["defeat"], loops=-1)
        elif key == "defeat":
            self.ch_ingame.set_volume(0.0)
            self.ch_shop.set_volume(0.0)
            if self.ch_defeat:
                self.ch_defeat.set_volume(0.0 if self.music_muted else 1.0)
                self.ch_defeat.play(self.music_tracks["defeat"], loops=-1)

        self.current_music_key = key
        self.music_playing = True

    def switch_music(self, new_key: str, sync_position: bool = True) -> None:
        """Cambia a otra pista con crossfade suave entre canales sincronizados."""
        if new_key not in self.music_tracks:
            return
        if new_key == self.current_music_key:
            return

        if not sync_position or not self.music_playing:
            self.play_music(new_key)
            return

        if new_key == "shop":
            self.crossfade_from_channel = self.ch_ingame
            self.crossfade_to_channel = self.ch_shop
        elif new_key == "ingame":
            self.crossfade_from_channel = self.ch_shop
            self.crossfade_to_channel = self.ch_ingame
        elif new_key == "defeat":
            if self.current_music_key == "shop":
                self.crossfade_from_channel = self.ch_shop
            else:
                self.crossfade_from_channel = self.ch_ingame
            self.crossfade_to_channel = self.ch_defeat
        else:
            self.play_music(new_key)
            return

        self.crossfade_active = True
        self.crossfade_timer = 0.0
        self.current_music_key = new_key

    def _stop_all_music(self) -> None:
        """Detiene todos los canales de música."""
        self.ch_lobby.stop()
        self.ch_ingame.stop()
        self.ch_shop.stop()
        if self.ch_defeat:
            self.ch_defeat.stop()
        self.music_playing = False
        self.crossfade_active = False

    def play_chips(self) -> None:
        """Reproduce un efecto de sonido de fichas."""
        if self.sfx_chips:
            snd = random.choice(self.sfx_chips)
            snd.play()

    def play_mult(self) -> None:
        """Reproduce un efecto de sonido de multiplicador."""
        if self.sfx_mult:
            snd = random.choice(self.sfx_mult)
            snd.set_volume(max(0.8, self.sfx_volume))
            snd.play()

    def play_coin(self) -> None:
        """Reproduce un efecto de sonido de monedas."""
        if self.sfx_coins:
            snd = random.choice(self.sfx_coins)
            snd.play()

    def play_win(self) -> None:
        """Reproduce el sonido de victoria de partida."""
        if self.sfx_win:
            self.sfx_win.play()

    def fadeout_music(self, duration_ms: int = 1500) -> None:
        """Detiene suavemente la música con un fade out sutil."""
        try:
            self.ch_lobby.fadeout(duration_ms)
            self.ch_ingame.fadeout(duration_ms)
            self.ch_shop.fadeout(duration_ms)
            if self.ch_defeat:
                self.ch_defeat.fadeout(duration_ms)
        except Exception:
            self._stop_all_music()
        self.music_playing = False
        self.crossfade_active = False

    def play_game_over(self) -> None:
        """Reproduce el sonido whoosh_long y realiza un crossfade sincronizado a music3 (derrota)."""
        if self.sfx_whoosh_long:
            self.sfx_whoosh_long.set_volume(self.sfx_volume)
            self.sfx_whoosh_long.play()

        if "defeat" in self.music_tracks and self.ch_defeat:
            self.switch_music("defeat", sync_position=True)
        else:
            self.fadeout_music(1500)

    def update(self, dt: float) -> None:
        """Actualiza el estado de la música y gestiona la transición crossfade."""
        if not self.crossfade_active:
            return

        self.crossfade_timer += dt
        progress = min(self.crossfade_timer / self.crossfade_duration, 1.0)
        t = progress * progress * (3.0 - 2.0 * progress)

        if self.crossfade_from_channel and self.crossfade_to_channel:
            self.crossfade_from_channel.set_volume(1.0 - t)
            self.crossfade_to_channel.set_volume(t)

        if progress >= 1.0:
            if self.crossfade_from_channel and self.crossfade_to_channel:
                self.crossfade_from_channel.set_volume(0.0)
                self.crossfade_to_channel.set_volume(1.0)
            self.crossfade_active = False

    def set_music_volume(self, vol: float) -> None:
        """Establece el volumen general de la música (0.0 - 1.0)."""
        self.music_volume = max(0.0, min(1.0, vol))
        for track in self.music_tracks.values():
            track.set_volume(self.music_volume)

    def set_sfx_volume(self, vol: float) -> None:
        """Establece el volumen de los efectos de sonido (0.0 - 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, vol))
        for snd in self.sfx_chips + self.sfx_mult + self.sfx_coins:
            snd.set_volume(self.sfx_volume)
        if self.sfx_win:
            self.sfx_win.set_volume(self.sfx_volume)
