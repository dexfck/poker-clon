# Documentación Técnica del Proyecto Poker2 (Clon de Balatro)

Esta documentación describe la arquitectura, estructura de archivos, módulos y flujo de ejecución del proyecto **Poker2**, desarrollado en Python utilizando la librería **Pygame-ce**.

---

## 1. Arquitectura del Sistema

El proyecto sigue una arquitectura **Módulo-Escena (MVC / State Machine)** bien desacoplada:

- **Core / GameState**: Mantiene el estado persistente de la partida (dinero, mazo, mano actual, comodines equipados, ciega actual, puntaje acumulado y estadísticas).
- **Engine**: Módulos de lógica de juego (evaluador de manos de póker, generador de ciegas/jefes, gestor de economía y reproductor de sonido con crossfade sutil y sincronizado).
- **UI / Effects**: Componentes visuales interactivos (cartas con física/animación, comodines con tooltip, botones estilizados, contadores numéricos animados, partículas, temblor de cámara y shader CRT).
- **Screens / ScreenManager**: Gestor central de pantallas que controla las transiciones entre el menú, selección de ciegas, gameplay, tienda, victoria, derrota y modo debug.

---

## 2. Estructura de Directorios

```
poker2/
├── main.py                    # Punto de entrada principal y bucle de juego
├── assets.py                  # Carga y gestión centralizada de texturas y fuentes
├── settings.py                # Constantes de configuración, colores y resolución de diseño (960x540)
├── DOCUMENTACION.md           # Documentación técnica completa del proyecto
│
├── core/                      # Estado del juego y estructura del mazo
│   ├── game_state.py          # Clase GameState (estado global de la partida)
│   └── deck.py                # Clase Deck (mazo estándar de 52 cartas)
│
├── engine/                    # Motores de juego y lógica pura
│   ├── evaluator.py           # Evaluador de combinaciones de póker
│   ├── poker_hands.py         # Mapeo y cálculo de fichas base / multiplicadores
│   ├── blinds.py              # Gestor de Ciegas (Pequeña, Grande y 5 Jefes)
│   ├── economy.py             # Cálculo de recompensas e intereses de fin de ronda
│   └── sound_manager.py       # Gestor de efectos SFX y pistas de música sincronizadas
│
├── entities/                  # Entidades del juego
│   ├── card.py                # Entidad Carta (palo, rango, fichas base, estados debuffed/face_down)
│   └── joker.py               # Definición de 25 Comodines oficiales y sus efectos (apply)
│
├── ui/                        # Componentes gráficos e interactivos de UI
│   ├── ui_element.py          # Clase base para elementos de interfaz
│   ├── button.py              # Botones estilizados con colores de hover y callbacks
│   ├── panel.py               # Contenedores redondeados y bordes tipo Balatro
│   ├── card_sprite.py         # Componente visual interactivo para cartas (animación y recortes)
│   ├── joker_sprite.py        # Componente visual para comodines
│   ├── counter.py             # Contador numérico con animación fluida de subida
│   └── tooltip.py             # Ventana emergente flotante para descripciones de comodines
│
├── effects/                   # Efectos visuales y shaders
│   ├── background.py          # Fondo animado de vórtice matemáticamente generado
│   ├── crt_shader.py          # Shader CRT opcional (efecto retro scanlines y curvatura)
│   ├── particles.py           # Sistema de partículas para popups de puntuación y explosiones
│   ├── screen_shake.py        # Efecto de sacudida de pantalla al calcular puntuación
│   └── round_clear_modal.py   # Modal animado de resumen de ronda superada
│
└── screens/                   # Pantallas del juego
    ├── screen_manager.py      # Gestor de cambio de pantallas
    ├── title_screen.py        # Pantalla de título inicial
    ├── main_menu.py           # Menú principal del juego
    ├── blind_select.py        # Pantalla de selección de Ciegas (con bloqueo de ciegas pasadas)
    ├── gameplay_screen.py     # HUD principal de juego y animación paso a paso de puntuación
    ├── shop_screen.py         # Tienda para comprar comodines y consumir
    ├── collection_screen.py   # Colección y álbum de comodines desbloqueados
    ├── settings_screen.py     # Menú de opciones (Música, Sonido, Shader CRT)
    ├── game_over.py           # Pantalla de derrota / Fin de partida (sonido whoosh_long y music3)
    ├── win_screen.py          # Pantalla de victoria tras superar Ante 8
    └── debug_screen.py        # Pantalla de pruebas (F1) para saltar a cualquier escena o probar jefes
```

---

## 3. Descripción de Módulos Principales

### 3.1. Entrada y Configuración Global
- **[main.py](file:///home/dexpider/Workspace/INTRODUCCION_PROGRAMACION_PROYECTOS/poker2/main.py)**: Inicializa Pygame, crea la ventana en resolución lógica `960x540` con escalado dinámico, gestiona el bucle de eventos (quit, tecla `F1` para Modo Debug), actualiza y renderiza el lienzo principal con el shader CRT.
- **[settings.py](file:///home/dexpider/Workspace/INTRODUCCION_PROGRAMACION_PROYECTOS/poker2/settings.py)**: Contiene la paleta de colores HSL/Balatro (`C.CHIPS_BLUE`, `C.MULT_RED`, `C.MONEY_GOLD`), constantes de dimensiones (`CARD_W`, `CARD_H`) y valores de cartas.
- **[assets.py](file:///home/dexpider/Workspace/INTRODUCCION_PROGRAMACION_PROYECTOS/poker2/assets.py)**: Carga las hojas de sprites (`8BitDeck_opt2.png` para cartas de Alto Contraste, `Jokers.png`, `BlindChips.png`, `Enhancers.png`), fuentes Tipográficas y devuelve subsuperficies recortadas en memoria.

### 3.2. Núcleo del Estado del Juego
- **[core/game_state.py](file:///home/dexpider/Workspace/INTRODUCCION_PROGRAMACION_PROYECTOS/poker2/core/game_state.py)**: Centraliza el estado completo de la partida actual:
  - Maneja la mano de cartas en posesión (`self.hand`), las cartas seleccionadas (`self.selected_cards`) y el mazo de robar (`self.draw_pile`).
  - Mantiene el conjunto de cartas jugadas en el Ante actual (`played_cards_this_ante`) para validar las reglas de la ciega de *El Pilar*.
  - Administra el dinero (`dollars`), comodines equipados (`jokers`), ante actual y reinicios de partida (`reset_run`).

### 3.3. Entidades y Comodines
- **[entities/card.py](file:///home/dexpider/Workspace/INTRODUCCION_PROGRAMACION_PROYECTOS/poker2/entities/card.py)**: Representa cada carta con su palo, rango, valor en fichas (`chips`) y propiedades de estado (`debuffed`, `is_face_down`). Retorna 0 fichas si está debilitada por un Jefe.
- **[entities/joker.py](file:///home/dexpider/Workspace/INTRODUCCION_PROGRAMACION_PROYECTOS/poker2/entities/joker.py)**: Define 25 clases de comodines oficiales adaptados de las reglas de Balatro (*Comodín*, *Glotón*, *Avaricioso*, *Lujurioso*, *Iracundo*, *Alegre*, *Loco*, *Equis*, *Impar*, *Gros Michel*, *Cavendish*, *Estandarte*, *Cumbre Mística*, *Acróbata*, *Abstracto*, etc.). Cada comodín implementa el método `apply(chips, mult, context)` retornando el nuevo cálculo.

### 3.4. Motor de Juego y Audio
- **[engine/blinds.py](file:///home/dexpider/Workspace/INTRODUCCION_PROGRAMACION_PROYECTOS/poker2/engine/blinds.py)**: Define la progresión de Ciegas (Small, Big, Boss) y las 5 Ciegas Jefe principales (*El Anzuelo*, *El Pilar*, *La Rueda*, *El Muro*, *La Ventana*).
- **[engine/sound_manager.py](file:///home/dexpider/Workspace/INTRODUCCION_PROGRAMACION_PROYECTOS/poker2/engine/sound_manager.py)**: Administra la reproducción de audio SFX (fichas, multiplicadores, monedas, victoria y `whoosh_long`) y pistas de música (`lobby`, `ingame`, `shop`, `defeat` con `music3.ogg`) utilizando canales dedicados para crossfade continuo en el mismo segundo/minuto exacto de reproducción.

### 3.5. Interfaz Visual e Interacción en Pantalla
- **[screens/gameplay_screen.py](file:///home/dexpider/Workspace/INTRODUCCION_PROGRAMACION_PROYECTOS/poker2/screens/gameplay_screen.py)**: La pantalla principal del juego. Contiene la máquina de estados de puntuación animada:
  1. `LIFT_PLAYED`: Elevación visual de las cartas seleccionadas.
  2. `SCORE_CARDS`: Suma pausada paso a paso de las fichas de cada carta con efectos de audio y popups.
  3. `SCORE_JOKERS`: Evaluación secuencial de comodines. **Únicamente los comodines que cumplen su condición rebotan, emiten sonido y muestran popup**.
  4. `CALCULATE`: Impacto final en el puntaje, vibración de cámara y recarga de mano.
  - Muestra la descripción flotante del efecto del Jefe activo en texto color rojo claro centrado bajo la barra de comodines.
  - Ejecuta la animación de descarte visible al jugar contra el jefe *El Anzuelo*.

---

## 4. Modo Debug (Acceso por Tecla F1)

El archivo **[screens/debug_screen.py](file:///home/dexpider/Workspace/INTRODUCCION_PROGRAMACION_PROYECTOS/poker2/screens/debug_screen.py)** proporciona una consola visual de desarrollo:

- **Salto Directo de Pantallas**: Botones para acceder inmediatamente a *Título*, *Menú Principal*, *Selección de Ciega*, *Gameplay*, *Tienda*, *Colección*, *Opciones*, *Fin de Partida* y *Victoria*.
- **Manipulación de Estado**: Adición instantánea de +$50 de dinero, asignación de comodines aleatorios y reinicio de partida.
- **Selector de Jefes (Boss Tester)**: 5 botones dedicados (*Anzuelo*, *Pilar*, *Rueda*, *Muro*, *Ventana*) para forzar el inicio inmediato de una partida contra cualquier Ciega Jefe específica.

---

## 5. Instrucciones de Ejecución

Para iniciar el videojuego:

```bash
python main.py
```
