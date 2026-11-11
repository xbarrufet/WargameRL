# Tasks

## 1. Control i puntuació d’objectius

- [x] 1.1 Extreure el càlcul de control per objectiu, filtrant robots destruïts i aplicant `objective_radius`; verificar majoria, empat i absència de robots amb tests de puntuació.
- [x] 1.2 Integrar la puntuació de l’equip actiu al final de `SCORING` amb `objective_points_for`; verificar zones friendly, neutral i enemy i que l’equip inactiu no puntua.
- [x] 1.3 Verificar que cada objectiu puntua una sola vegada per transició de torn i que pot tornar a puntuar en torns consecutius mentre el control es manté.

## 2. Estat de final i serialització

- [x] 2.1 Afegir l’estat de final pendent i les dades necessàries per serialitzar-lo; verificar un round trip durant el torn que el segon equip encara ha de completar.
- [x] 2.2 Implementar la comparació final i l’assignació de `TEAM_A_WINS`, `TEAM_B_WINS` o `DRAW`; verificar els tres resultats amb puntuacions controlades.
- [x] 2.3 Bloquejar accions i `EndPhaseAction` quan `GameResult` ja no és `PENDING`; verificar que l’estat final no es modifica.

## 3. Final anticipat i límit de rondes

- [x] 3.1 Detectar quan el primer equip arriba a `victory_points` i permetre que el segon completi el seu torn de la ronda; verificar que el resultat només es fixa després del torn corresponent.
- [x] 3.2 Tancar immediatament després que el segon equip arribi al llindar en el seu torn; verificar que no s’inicia una ronda nova.
- [x] 3.3 Aplicar el límit de 15 rondes després de `SCORING` del segon equip i verificar victòria o empat per puntuació final.
- [x] 3.4 Afegir regressions de la seqüència completa `MOVEMENT → SHOOTING → SCORING` amb puntuació i final, i verificar que les regles configurades continuen disponibles.

## 4. Documentació i verificació

- [x] 4.1 Actualitzar `docs/FASES_IMPLEMENTACIO.md`, `docs/DESCRIPCIO.md` i `docs/DOCUMENT_TECNIC.md` amb el control, la victòria, l’empat i el límit de rondes, i verificar coherència amb `docs/GAME_RULES.md`.
- [x] 4.2 Executar `PYTHONPATH=src .venv/bin/pytest -q` i `openspec validate --changes --strict --no-interactive`; resoldre qualsevol regressió abans de donar el canvi per implementable.
