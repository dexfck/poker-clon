@echo off
title Compilador de Poker2 para Windows (Poker2.exe Autonomo)
echo =========================================================================
echo   Compilador Automatico de Poker2.exe para Windows (Sin necesidad de Python)
echo =========================================================================
echo.

echo 1. Instalando dependencias necesarias para empaquetar...
pip install pygame-ce numpy pyinstaller

echo.
echo 2. Generando ejecutable standalone unico Poker2.exe...
pyinstaller --noconfirm --onefile --windowed --name "Poker2" --add-data "assets;assets" --add-data "resources;resources" main.py

echo.
echo =========================================================================
echo   COMPILACION COMPLETADA CON EXITO!
echo   El archivo ejecutable independiente se encuentra en:
echo   dist\Poker2.exe
echo.
echo   Este archivo Poker2.exe es 100%% AUTONOMO.
echo   Cualquier usuario puede jugarlo en Windows SIN INSTALAR PYTHON.
echo =========================================================================
echo.
pause
