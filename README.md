# 🃏 Poker2 – Clon de Balatro en Pygame

[![Build Executables](https://github.com/dexfck/poker-clon/actions/workflows/build.yml/badge.svg)](https.github.com/dexfck/poker-clon/actions/workflows/build.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pygame-ce](https://img.shields.io/badge/pygame--ce-2.5%2B-green.svg)](https://pyga.me/)

**Poker2** es una recreación fiel y moderna estilo *roguelike de póker* inspirada en **Balatro**, desarrollada en Python con la librería **Pygame-ce**. Combina mecánicas de póker tradicional con Comodines especiales (*Jokers*), Ciegas Jefe (*Boss Blinds*), efectos retro de CRT, banda sonora dinámica sincronizada con crossfade y tienda de artículos.

---

## ✨ Características Principales

- **🃏 25 Comodines Oficiales**: Implementación de comodines aditivos (+Fichas, +Mult) y multiplicativos (XMult) con animaciones de rebote, sonido y popups condicionales.
- **👹 5 Ciegas Jefe (Boss Blinds)**:
  - **El Anzuelo (*The Hook*)**: Descarta 2 cartas aleatorias en vivo por cada mano jugada (con animación visual de descarte).
  - **El Pilar (*The Pillar*)**: Debilita con una marca `X` roja las cartas jugadas anteriormente durante el mismo Ante.
  - **La Rueda (*The Wheel*)**: Reparte 1 de cada 7 cartas boca abajo.
  - **El Muro (*The Wall*)**: Requiere el doble de puntuación objetivo.
  - **La Ventana (*The Window*)**: Debilita todas las figuras (J, Q, K).
- **🎨 Mazo de Alto Contraste (High Contrast)**: Cartas renderizadas con la baraja oficial `8BitDeck` de alto contraste.
- **📺 Shader CRT Retro y Efecto Vórtice**: Renderizado con distorsión curva CRT y fondo de vórtice matemático en tiempo real.
- **🎵 Motor de Audio Sincronizado**: Pistas musicales (`lobby`, `ingame`, `shop`, `defeat` con `music3.ogg`) sincronizadas al milisegundo con *crossfade* suave entre pantallas.
- **🏆 Pantalla de Victoria y Derrota**: Pantalla de resumen de victoria tras superar el Ante 8 y pantalla de derrota con sonido `whoosh_long`.
- **🛠️ Modo Debug Integrado (`Tecla F1`)**: Consola visual para saltar entre escenas, inyectar dinero, probar comodines y probar cualquier Ciega Jefe instantáneamente.

---

## 🎮 Controles

| Tecla / Acción | Función |
|---|---|
| **Clic Izquierdo** | Seleccionar / Deseleccionar Carta |
| **Boton "JUGAR MANO"** | Evaluar mano seleccionada |
| **Boton "DESCARTAR"** | Descartar cartas seleccionadas |
| **Ord. Rango / Ord. Palo** | Ordenar cartas de la mano |
| **Tecla `F1`** | Abrir / Cerrar Modo Debug |
| **Tecla `ESC`** | Menú de Opciones / Pausa |

---

## 🚀 Descarga y Ejecución

### 💾 Opción 1: Ejecutable para Windows (`Poker2.exe`)
Puedes descargar el ejecutable portátil para Windows (sin necesidad de tener Python instalado) directamente desde la pestaña de **[Actions / Artifacts](https://github.com/dexfck/poker-clon/actions)** de GitHub.

### 🐍 Opción 2: Ejecutar desde Código Fuente (Python)

1. **Clonar el repositorio:**
   ```bash
   git clone git@github.com:dexfck/poker-clon.git
   cd poker-clon
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/macOS
   # venv\Scripts\activate   # En Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Iniciar el juego:**
   ```bash
   python main.py
   ```

---

## 📄 Documentación Técnica

Para conocer la arquitectura interna del sistema, el flujo de la máquina de estados de puntuación o la lista completa de clases y módulos, consulta el archivo:

📖 **[DOCUMENTACION.md](DOCUMENTACION.md)**

---

## 🛠️ Compilar Ejecutable Localmente

### En Windows (`.exe` de 1 clic)
Ejecuta el script automático de compilación:
```cmd
build_windows_exe.bat
```
El archivo `Poker2.exe` se generará en la carpeta `dist/`.

### En Linux
```bash
pyinstaller --noconfirm --onefile --name "Poker2-Linux" --add-data "assets:assets" --add-data "resources:resources" main.py
```

---

## 📜 Licencia y Créditos

Desarrollado como proyecto académico de programación. Basado en el concepto original de **Balatro** de *LocalThunk*.
