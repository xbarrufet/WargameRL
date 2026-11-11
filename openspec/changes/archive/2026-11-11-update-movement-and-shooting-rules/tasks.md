# Tasks

## 1. Esquema i model

- [x] 1.1 Afegir `jump: 4` i `hit_target: 4` a `config/example.yaml`, `RobotConfig`, `Robot` i la serialització; verificar un round trip complet.
- [x] 1.2 Validar els dos camps com a enters positius i afegir tests de camps absents, tipus invàlid i valors no positius.
- [x] 1.3 Actualitzar i validar els paràmetres globals del YAML: `objective_radius: 2`, `minimum_objective_distance: 5`, `robot_max_damage: 5`, `robot_destruction_points: 3`, `victory_points: 15` i `objective_points: 1/3/5`.
- [x] 1.4 Resoldre explícitament les decisions pendents de `docs/GAME_RULES.md` abans d’implementar geometria d’arcs, línia de visió, bloqueig per robots, coordenades i límit de rondes. La correspondència `300° → NW` corregeix la duplicació `NE` del text original.

## 2. Moviment

- [x] 2.1 Implementar la regla de córrer amb límit `M`, direcció frontal, elevació vàlida, pivots i bloqueig per robots; verificar rutes vàlides i rebutjades.
- [x] 2.2 Implementar la regla de saltar amb límit `J`, qualsevol elevació/direcció, travessa d’obstacles i orientació final; verificar que el destí no sigui ocupat.

## 3. Dispar i cobertura

- [x] 3.1 Implementar la tirada `1D6 >= H` amb modificadors `+1` si no ha mogut i `-2` si ha saltat; verificar resultats reproduïbles amb llavor.
- [x] 3.2 Eliminar la cobertura per elevació de les regles, documentació i tests; verificar que un blanc elevat no rep cap bonificació.

## 4. Documentació i integració

- [x] 4.1 Actualitzar `DESCRIPCIO.md`, `DOCUMENT_TECNIC.md`, `FASES_IMPLEMENTACIO.md` i `config/example.yaml` amb el nou contracte.
- [x] 4.2 Executar `PYTHONPATH=src .venv/bin/pytest -q` i `openspec validate --changes --strict --no-interactive` sense regressions.
