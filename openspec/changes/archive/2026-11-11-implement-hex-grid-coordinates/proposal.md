# Proposal

## Why

La fase 2 ja representa el tauler i les entitats amb coordenades `q,r`, però
`HexCoordinate` encara no ofereix les operacions geomètriques que necessiten el
motor i la futura UI. Cal centralitzar aquesta geometria ara per evitar que la
distància, els veïns o la conversió visual es reimplementin de manera
inconsistent en moviment, visió i interfície.

## What Changes

- Afegir operacions de veïnatge i distància hexagonal per a coordenades axials `q,r`.
- Validar coordenades contra les dimensions del tauler i consultar elevacions.
- Exposar la detecció d’ocupació del tauler a partir de l’estat actual.
- Implementar conversió entre coordenades i píxels per a hexàgons **flat-top**,
  amb origen i mida de hexàgon configurables.
- Implementar la conversió inversa píxel → coordenada amb arrodoniment hexagonal
  i indicar quan el punt queda fora del tauler.
- Afegir proves unitàries i documentació de les convencions geomètriques.

## Capabilities

### New Capabilities

- `hex-grid-geometry`: operacions deterministes de coordenades, tauler,
  elevacions, ocupació i conversió flat-top entre mapa i pantalla.

### Modified Capabilities

Cap.

## Impact

- `src/wargame/model/coordinates.py` i possibles utilitats de tauler.
- `Board`/`GameState` per consultar límits, elevacions i ocupació.
- Nous tests de geometria i conversió de pantalla.
- `docs/FASES_IMPLEMENTACIO.md` i `docs/DOCUMENT_TECNIC.md` per fixar la
  convenció flat-top.
- No s’afegeix dependència de Pygame al model ni al motor.
