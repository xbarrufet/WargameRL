# Tasks

## 1. CLI i adaptador de consola

- [x] 1.1 Definir la subcomanda `simulate` i les opcions `--config`, `--seed` i `--mode`, mantenint `--version`; verificar-ho amb proves del parser i ajuda del CLI.
- [x] 1.2 Implementar la càrrega de configuració i la creació de `GameState` amb resolució determinista de la ruta per defecte; verificar errors de ruta/YAML amb codi de sortida no zero.
- [x] 1.3 Crear el formatter de snapshots, transicions, combat, puntuació i resultat final; verificar que la sortida inclou llavor, ronda, fase, equip actiu i puntuacions.

## 2. Mode demo i reproduïbilitat

- [x] 2.1 Implementar la seqüència demo composant només accions públiques del motor i adaptant-se a les accions vàlides de `config/example.yaml`; verificar que una execució no interactiva arriba a un resultat terminal.
- [x] 2.2 Connectar la llavor del CLI amb `GameState` i la resolució aleatòria existent; verificar que dues execucions equivalents amb la mateixa llavor produeixen els mateixos resums i resultat.
- [x] 2.3 Mostrar explícitament el tancament per llindar de victòria, final de ronda i límit de 15 rondes; verificar cada causa amb escenaris controlats.

## 3. Mode manual i documentació

- [x] 3.1 Implementar el parser de les ordres manuals, inclosos `help` i `quit`, i delegar la legalitat al motor; verificar que una ordre vàlida actualitza l’estat i una d’invàlida no el muta.
- [x] 3.2 Definir al `docs/DOCUMENT_TECNIC.md` la gramàtica i totes les comandes de text possibles del mode manual, inclosos arguments i fases aplicables; verificar que el document coincideix amb el parser implementat.
- [x] 3.3 Afegir documentació d’ús del CLI amb exemples de mode demo, llavor, configuració i mode manual; verificar que les ordres documentades coincideixen amb `--help`.
- [x] 3.4 Afegir proves d’integració amb stdin/stdout/stderr injectats per a càrrega, demo, errors i manual; verificar que tota la suite existent continua passant amb `pytest`.
- [x] 3.5 Fer que `status` mostri l’identificador, l’equip, la posició `(q,r)` i l’estat de destrucció de cada robot; verificar-ho amb una prova del mode manual.

## 4. Integració

- [x] 4.1 Executar el CLI instal·lat amb `config/example.yaml` i una llavor fixa, revisar la sortida completa i corregir qualsevol dependència accidental de Pygame; verificar l’execució amb una ordre documentada.
- [x] 4.2 Executar `openspec validate implement-console-simulation --strict` i deixar tots els artefactes i proves preparats per a revisió.
