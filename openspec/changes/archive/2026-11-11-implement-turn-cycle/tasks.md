# Tasks

## 1. Accions i validació de fases

- [x] 1.1 Definir `EndPhaseAction` i els resultats/errors de transició, i verificar que només accepten fases i equips coherents.
- [x] 1.2 Implementar la validació de l’equip actiu i de la fase per a les accions del motor, i verificar el rebuig atòmic d’accions incorrectes.
- [x] 1.3 Conservar un `RulesConfig` immutable dins de `GameState`, integrar-lo en `from_config`, `to_dict` i `from_dict`, i verificar el round trip de les regles.

## 2. Màquina de torn

- [x] 2.1 Implementar les transicions `MOVEMENT → SHOOTING → SCORING → MOVEMENT` i verificar que l’equip actiu es conserva fins al final de `SCORING`.
- [x] 2.2 Integrar la puntuació de l’equip actiu abans del canvi d’equip i verificar que la ronda només augmenta quan tots dos equips han completat el torn.
- [x] 2.3 Conservar l’ordre lliure dels robots dins de cada fase i verificar que robots del mateix equip poden actuar en qualsevol ordre.

## 3. Integració i documentació

- [x] 3.1 Actualitzar exports, documentació tècnica i la fase 5 amb l’API de transició, i verificar que no introdueix dependències de Pygame o IA.
- [x] 3.2 Afegir proves d’integració del cicle complet i executar `PYTHONPATH=src .venv/bin/pytest -q` sense regressions.
- [x] 3.3 Executar `openspec validate --changes --strict --no-interactive` i verificar que totes les especificacions i tasques són coherents.
