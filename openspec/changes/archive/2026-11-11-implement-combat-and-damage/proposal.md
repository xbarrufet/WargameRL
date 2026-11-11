# Proposal

## Why

La fase 7 define les regles de combat, però el motor encara no pot executar
un dispar complet ni resoldre el dany de manera reproduïble. Implementar-ho ara
connecta la línia de visió existent amb el cicle de torn i permet validar la
simulació completa abans de la puntuació i la interfície.

## What Changes

- Afegir una acció de dispar vàlida només durant `SHOOTING`, per a robots de
  l’equip actiu i com a màxim una vegada per torn.
- Validar que el blanc enemic és visible, frontal i dins del rang configurat.
- Resoldre la tirada d’impacte `1D6 >= H` amb els modificadors de moviment
  definits per les regles (`+1` quiet, `0` moviment normal, `-2` salt).
- Resoldre `D` daus de salvació segons l’arc atacat i els valors d’armadura
  frontal, lateral i posterior.
- Acumular impactes, retirar robots destruïts amb `robot_max_damage` i concedir
  `robot_destruction_points` una sola vegada a l’equip atacant.
- Centralitzar l’atzar i permetre llavors reproduïbles; retornar un resum
  inspectable de cada combat.
- Actualitzar l’estat serialitzable, les proves i la documentació necessària.

## Capabilities

### New Capabilities

- `combat-resolution`: executa dispars, tirades d’impacte, salvacions, dany,
  destrucció i recompensa per robot destruït.

### Modified Capabilities

- `turn-cycle`: el dispar passa a ser una acció de fase `SHOOTING` i queda
  limitat a una execució per robot i torn.
- `game-state-model`: l’estat conserva el progrés de dispar dels robots i els
  resultats necessaris per mantenir la resolució i la serialització coherents.

## Impact

- `src/wargame/engine/` i `src/wargame/rules/` per a l’acció i la resolució del
  combat.
- `src/wargame/model/entities.py` i `src/wargame/model/state.py` per al dany,
  destrucció, seguiment per torn i round trip JSON.
- `src/wargame/engine/turn.py` per a les restriccions de fase i equip.
- `config/example.yaml`, documentació i tests de combat deterministes.
- No s’introdueix cap dependència del motor respecte de Pygame o dels agents AI.
