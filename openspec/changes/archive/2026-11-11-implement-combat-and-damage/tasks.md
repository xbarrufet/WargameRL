# Tasks

## 1. Estat de combat i aleatorietat

- [x] 1.1 Afegir al model el registre de robots que ja han disparat, amb valor inicial buit, i verificar amb un test que una partida nova no conté dispars.
- [x] 1.2 Afegir la serialització i restauració del registre de dispars, impactes i destrucció, i verificar un round trip JSON dins del mateix torn.
- [x] 1.3 Centralitzar el generador de daus amb una llavor reproduïble i verificar que dues resolucions equivalents produeixen les mateixes tirades.

## 2. Resolució del dispar

- [x] 2.1 Crear `ShootAction` i la validació de fase, equip, robot no destruït i límit d’un dispar per torn; verificar errors atòmics en fases o equips incorrectes i en el segon dispar.
- [x] 2.2 Connectar la validació amb `assess_target` i verificar blancs aliats, fora d’arc, fora de rang, bloquejats i destruïts amb els motius existents.
- [x] 2.3 Implementar la tirada d’impacte `1D6 >= H` amb modificadors `+1`, `0` i `-2`; verificar cada cas i el resum retornat.
- [x] 2.4 Implementar les salvacions `D`, l’armadura segons l’arc atacat i el recompte d’impactes; verificar frontal, lateral, posterior, impacte fallit i múltiples salvacions.

## 3. Dany, destrucció i integració del torn

- [x] 3.1 Aplicar impactes al defensor, marcar-lo destruït en arribar a `robot_max_damage` i excloure’l d’ocupació i blancs; verificar la retirada lògica i el bloqueig d’accions posteriors.
- [x] 3.2 Concedir `robot_destruction_points` una sola vegada a l’equip atacant i verificar que no es tornen a concedir en cap resolució posterior.
- [x] 3.3 Reiniciar el registre de dispars en començar el torn següent i verificar que cada robot pot tornar a disparar una vegada després del canvi d’equip.
- [x] 3.4 Afegir proves de regressió de fase completa (`MOVEMENT → SHOOTING → SCORING`) i conservar la independència del motor respecte de Pygame.

## 4. Documentació i verificació

- [x] 4.1 Actualitzar `docs/FASES_IMPLEMENTACIO.md`, `docs/DESCRIPCIO.md` i la documentació tècnica amb el contracte implementat, i verificar que no contradiguin `docs/GAME_RULES.md`.
- [x] 4.2 Executar `PYTHONPATH=src .venv/bin/pytest -q` i `openspec validate --changes --strict --no-interactive`; resoldre qualsevol regressió abans de donar la proposta per implementable.
