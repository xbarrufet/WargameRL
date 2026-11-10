# Proposal

## Why

La configuració YAML ja es pot validar, però encara no existeix un model de
partida que permeti treballar amb aquest resultat. La fase 2 ha de convertir la
configuració en un estat explícit, serialitzable i preparat per a les regles de
les fases següents.

## What Changes

- Definir coordenades hexagonals, orientacions i fases de partida.
- Definir les entitats `Team`, `Robot`, `Objective` i `Board`.
- Definir `GameState` amb torn, fase, equip actiu, puntuacions, danys i resultat.
- Crear l’estat inicial a partir de la configuració validada de la fase 1.
- Afegir serialització i deserialització deterministes per inspecció i proves.
- Validar invariants del model, incloent identificadors, ocupació i valors inicials.

## Capabilities

### New Capabilities

- `game-state-model`: representa l’estat complet i serialitzable d’una partida
  abans d’aplicar les regles d’accions.

### Modified Capabilities

Cap.

## Impact

- Nous mòduls sota `src/wargame/model/`.
- Integració amb `GameConfig` de `wargame.io.yaml_reader`.
- Nous tests de model i serialització.
- No s’implementen encara moviment, combat, puntuació ni geometria hexagonal
  avançada de la fase 3.
