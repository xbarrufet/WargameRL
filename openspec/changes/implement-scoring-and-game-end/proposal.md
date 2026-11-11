# Proposal

## Why

El motor ja calcula el valor configurable d’un objectiu, però encara no
resol el control complet al final del torn ni tanca la partida quan es compleix
una condició de victòria. La fase 8 ha de convertir la puntuació parcial en un
cicle de partida complet i determinista, incloent-hi empats i el límit de 15
rondes.

## What Changes

- Calcular el control de cada objectiu al final de `SCORING` comptant robots no
  destruïts dins de `objective_radius`.
- Puntuar només l’equip actiu, amb empat de control sense puntuació i com a
  màxim una puntuació per objectiu i torn.
- Aplicar els valors configurats `friendly`, `neutral` i `enemy` segons la zona
  de l’objectiu.
- Activar el final quan un equip arriba a `victory_points`, permetent al segon
  equip completar el torn de la ronda quan correspongui.
- Aplicar el límit de 15 rondes i determinar `TEAM_A_WINS`, `TEAM_B_WINS` o
  `DRAW` comparant les puntuacions finals.
- Bloquejar noves accions i transicions incompatibles quan la partida ja ha
  acabat, mantenint el resultat serialitzable.
- Afegir proves de control, empat, puntuació repetida, victòria anticipada,
  final de ronda, límit de rondes i empat final.

## Capabilities

### New Capabilities

- `game-end`: determina quan acaba la partida i quin resultat final correspon.

### Modified Capabilities

- `configurable-objective-scoring`: amplia el càlcul configurable amb control
  d’objectius, radi, empat i puntuació única per torn.
- `turn-cycle`: integra la puntuació al final de `SCORING`, el canvi de ronda i
  les transicions de final de partida.

## Impact

- `src/wargame/engine/turn.py` i `src/wargame/rules/scoring.py` per al control,
  puntuació i transicions.
- `src/wargame/model/state.py` i `src/wargame/model/enums.py` per al resultat,
  estat final i serialització.
- Tests de puntuació, torns i estat; documentació de la fase 8.
- No s’afegeixen dependències externes ni cap dependència respecte de Pygame o
  dels agents AI.
