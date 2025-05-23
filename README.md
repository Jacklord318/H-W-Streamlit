
# App de Visualización de Red Hidráulica (React + ReactFlow)

Este proyecto permite:
- Cargar datos hidráulicos de nodos y tramos.
- Calcular pérdidas de carga por Hazen-Williams.
- Sugerir diámetro económico.
- Visualizar velocidades y presiones en m.c.a. en los nodos.

## Archivos incluidos
- `HazenWilliamsApp.tsx` — Código principal React con lógica y visualización.
- `ejemplo_red_hidraulica.xlsx` — Archivo de ejemplo.
- `README.md` — Esta guía.

## Cómo usar
1. Importa `HazenWilliamsApp.tsx` en tu proyecto Vite + React.
2. Usa el archivo Excel de ejemplo o carga uno con las mismas columnas.
3. Visualiza el grafo con React Flow y verifica resultados.
