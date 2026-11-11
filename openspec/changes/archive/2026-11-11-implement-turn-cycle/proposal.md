# Proposal

## Why

El motor ja pot representar l’estat i executar moviment, però encara no pot
coordinar les fases d’un torn ni rebutjar accions fora de fase. La fase 5
necessita una màquina d’estats determinista que permeti avançar una partida
completa de moviment a dispar, puntuació i canvi d’equip.

## What Changes

- Implementar la seqüència `MOVEMENT → SHOOTING → SCORING` per al torn de
  l’equip actiu.
- Afegir `EndPhaseAction` per finalitzar explícitament cada fase.
- Validar que només l’equip actiu pot actuar i que cada acció correspon a la
  fase actual.
- Fer que al final de `SCORING` només puntui l’equip actiu i després canviï
  l’equip actiu; incrementar la ronda quan tots dos equips hagin completat el
  seu torn.
- Preservar l’ordre lliure dels robots dins de cada fase.
- Afegir proves de transicions, canvis d’equip, canvi de ronda i rebutjos per
  equip o fase incorrectes.

## Capabilities

### New Capabilities

- `turn-cycle`: màquina d’estats del torn, transicions de fase, equip actiu i
  validació de les accions segons la fase actual.

### Modified Capabilities

Cap.

## Impact

- Nous tipus d’acció i validació sota `src/wargame/engine/`.
- Integració amb `GameState`, `Phase`, equips, robots i les regles de
  puntuació existents.
- Nous tests de màquina d’estats i possibles ajustos de serialització si cal
  conservar informació del cicle.
- Cap dependència nova i cap canvi a Pygame, Micro AI o Macro AI.
