# Tasks

## 1. Geometria i resultats de visibilitat

- [x] 1.1 Definir les classificacions d’arc i els motius tipats de rebuig, i verificar les sis orientacions amb casos frontals, laterals i posteriors.
- [x] 1.2 Implementar la consulta de blancs candidats i el límit de rang `R`, i verificar que els blancs fora de rang són rebutjats amb un motiu determinista.

## 2. Línia de visió i elevacions

- [x] 2.1 Implementar el recorregut de la línia hexagonal i el bloqueig per elevacions segons les regles, i verificar casos baix-baix bloquejats i atacant elevat.
- [x] 2.2 Ignorar robots interposats sense ignorar el terreny, i verificar que un robot no bloqueja però una elevació alta sí que pot bloquejar.
- [x] 2.3 Integrar l’API amb `GameState`, `Board` i exports del motor sense dependències de Pygame, i verificar consultes pures sense mutació de l’estat.

## 3. Documentació i verificació

- [x] 3.1 Actualitzar la documentació tècnica i marcar la fase 6 com a completada, verificant que no introdueix cobertura per elevació ni regles de combat.
- [x] 3.2 Executar `PYTHONPATH=src .venv/bin/pytest -q` i verificar la suite completa amb els nous casos de visibilitat.
- [x] 3.3 Executar `openspec validate --changes --strict --no-interactive` i verificar que les especificacions i tasques són coherents.
