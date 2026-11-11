# Proposal

## Why

La simulació ja es pot executar i inspeccionar per consola, però encara no ofereix una representació espacial del mapa ni una manera visual de jugar-la. Aquesta fase aporta una UI Pygame que faci el motor accessible manualment sense duplicar-ne les regles.

## What Changes

- Afegir una finestra Pygame amb la graella hexagonal flat-top, elevacions i zones.
- Renderitzar objectius, robots, orientacions i sprites configurats.
- Permetre seleccionar robots i caselles amb el ratolí.
- Mostrar i actualitzar moviments accessibles, salts i blancs vàlids proporcionats pel motor.
- Mostrar fase, equip actiu, ronda, puntuacions, missatges d’error i resultat final, inclòs l’empat.
- Afegir un punt d’entrada gràfic que carregui una configuració YAML i delegui les accions al motor.
- Mantenir la UI desacoblada del motor i no reimplementar validacions de moviment, visibilitat, combat, puntuació o final de partida.

## Capabilities

### New Capabilities

- `pygame-visualization`: Interfície gràfica interactiva per consultar l’estat del joc, seleccionar entitats i executar accions mitjançant les API públiques del motor.

### Modified Capabilities

- None.

## Impact

- Afecta principalment `src/wargame/ui/` i el punt d’entrada CLI, amb proves de renderització i interacció separades del motor.
- Reutilitza `GameState`, la geometria hexagonal, les consultes de moviment/visibilitat i les accions existents.
- Utilitza la dependència Pygame ja declarada pel projecte i els sprites de `config/imgs` resolts per la configuració.
- No modifica el model de dades ni les regles del joc; pot requerir petites API de consulta o adaptació només si les existents no són suficients per a la UI.
