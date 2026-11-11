# Proposal

## Why

El motor ja pot moure robots i gestionar torns, però encara no pot determinar
quins blancs són visibles ni si es troben dins de l’arc frontal i del rang de
l’arma. La fase 6 necessita una capacitat de visibilitat independent de Pygame
que serveixi tant al motor com a la futura UI i al combat.

## What Changes

- Implementar el càlcul de l’arc frontal i posterior a partir de les sis
  orientacions del robot.
- Validar la distància màxima `R` de l’arma.
- Implementar la línia de visió amb bloqueig per elevacions segons
  `docs/GAME_RULES.md`.
- Fer que els robots no bloquegin la línia de visió.
- Retornar blancs vàlids i motius deterministes per als blancs rebutjats.
- Exposar la relació frontal, lateral o posterior necessària per a les fases
  posteriors, sense implementar encara el dispar ni el dany.
- Afegir proves de geometria d’arcs, rang, elevacions, robots interposats i
  errors de validació.

## Capabilities

### New Capabilities

- `line-of-sight`: càlcul d’arcs, visibilitat, rang i validació de blancs per al
  motor de joc.

### Modified Capabilities

Cap.

## Impact

- Nou mòdul de regles de visibilitat sota `src/wargame/rules/` i exports de
  l’API pública si cal.
- Integració amb `HexCoordinate`, `Direction`, `Board`, `Robot` i `GameState`.
- Nous tests independents de Pygame.
- Cap canvi a la resolució aleatòria de combat, armadures o IA.
