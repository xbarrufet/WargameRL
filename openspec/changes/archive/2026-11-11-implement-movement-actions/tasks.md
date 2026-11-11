# Tasks

## 1. Accions i resultats de moviment

- [x] 1.1 Definir les dades d'acció per a moviment normal, pivot i salt, amb validació de paràmetres i verificar-les amb tests de construcció i errors.
- [x] 1.2 Implementar el planificador de moviment normal amb avanços frontals, pivots, pressupost `M`, elevació i ocupació, i verificar rutes vàlides i rebutjades.
- [x] 1.3 Implementar el planificador de salt amb distància `J`, qualsevol elevació, travessa d'obstacles i destí lliure, i verificar casos dins i fora del límit.

## 2. Integració amb l'estat

- [x] 2.1 Integrar l'execució atòmica de les accions amb `GameState`, inclosa l'orientació gratuïta després del salt, i verificar que les accions invàlides no deixen efectes parcials.
- [x] 2.2 Exposar les destinacions accessibles i el tipus de moviment executat, i verificar que només inclou opcions vàlides per a l'estat actual.
- [x] 2.3 Afegir o actualitzar els exports públics del motor i verificar que l'API es pot importar sense Pygame.

## 3. Verificació i documentació

- [x] 3.1 Afegir proves de regressió per a robots destruïts, robots que bloquegen només el destí normal i objectius que no bloquegen el moviment, i verificar-les amb `PYTHONPATH=src .venv/bin/pytest -q`.
- [x] 3.2 Actualitzar la documentació tècnica de la fase 4 amb l'API i les decisions d'implementació, i verificar que no contradigui `docs/GAME_RULES.md`.
- [x] 3.3 Executar `PYTHONPATH=src .venv/bin/pytest -q` i `openspec validate --changes --strict --no-interactive` sense regressions.
