# Proposal

## Why

La fase 9 encara no té una manera executable d’inspeccionar una partida completa: el punt d’entrada només mostra un missatge pendent. Abans de construir la UI Pygame, cal una interfície de consola determinista que permeti validar el motor, el combat, la puntuació i les condicions de final amb `config/example.yaml`.

## What Changes

- Afegir una capacitat de simulació per consola que carregui una configuració YAML i creï un `GameState`.
- Ampliar el CLI amb una execució de prova completa i una opció de llavor aleatòria reproduïble.
- Mostrar l’estat inicial, les transicions de fase/torn, els resultats dels combats, les puntuacions i el resultat final.
- Fer que `status` mostri també la posició `(q,r)` i l’estat de cada robot.
- Permetre una seqüència d’accions manual o una seqüència de prova predefinida, sense duplicar les regles del motor.
- Fer explícit al resum quan la partida acaba anticipadament per punts o pel límit de rondes.

## Capabilities

### New Capabilities

- `console-simulation`: executar i inspeccionar una partida completa des de la línia d’ordres, amb mode de prova, entrada manual i reproduïbilitat per llavor.

### Modified Capabilities

Cap.

## Impact

- Afecta `src/wargame/cli.py` i pot afegir mòduls d’orquestració/adaptació de consola sota `src/wargame/`.
- Pot afegir proves d’integració del CLI i documentació d’ús.
- Reutilitza `yaml_reader`, `GameState` i les accions del motor; no introdueix regles noves ni dependència del motor amb Pygame.
- La sortida de consola esdevé una interfície observable nova, però les API del motor i les regles del joc es mantenen compatibles.
