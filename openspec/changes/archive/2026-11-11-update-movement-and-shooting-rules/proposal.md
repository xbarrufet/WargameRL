# Proposal

## Why

`docs/GAME_RULES.md` és ara la font de veritat de les regles: el moviment
diferencia córrer i saltar, i el dispar ja no impacta automàticament. El YAML
necessita conservar aquestes regles amb els nous valors per robot `jump` (`J`)
i `hit_target` (`H`), i cal retirar la cobertura per elevació.

## What Changes

- Afegir `jump` (`J`) i `hit_target` (`H`) a cada robot del YAML.
- Validar i carregar els dos valors al `RobotConfig` i al model `Robot`.
- Definir les regles de córrer i saltar segons `M` i `J`.
- Definir la tirada d’impacte `1D6 >= H` amb modificadors per no haver mogut
  (`+1`) i haver saltat (`-2`).
- Eliminar la cobertura per elevació de línia de visió i combat.
- Actualitzar documentació, fases, configuració d’exemple i tests.
- Actualitzar els paràmetres globals: radi de control `2`, distància mínima
  entre objectius `5`, vida màxima `5`, punts per destrucció `3`, punts per
  victòria `15` i punts d’objectius `1/3/5`.
- **BREAKING**: les configuracions antigues sense `jump` i `hit_target` deixaran
  de ser vàlides.

## Capabilities

### New Capabilities

- `movement-and-shooting-rules`: moviment de córrer/salt, resolució d’impacte i
  interacció amb la línia de visió sense cobertura per elevació.

### Modified Capabilities

Cap.

## Impact

- Esquema YAML i `RobotConfig` a `src/wargame/io/yaml_reader.py`.
- Model `Robot` i serialització de l’estat.
- Nous mòduls de regles de moviment i combat.
- `config/example.yaml`, documentació de regles i fases d’implementació.
- Tests de validació, moviment, impacte i absència de cobertura.
- Valors inicials de l’exemple: `M=3`, `J=4` i `H=4+` (`hit_target: 4`).
