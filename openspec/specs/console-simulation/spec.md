# console-simulation Specification

## Purpose

Aquesta capacitat permet executar i inspeccionar una partida completa sense
interfície gràfica, fent servir el motor existent i una sortida determinista.

## Requirements

### Requirement: Load a configured game from the console
El CLI SHALL permetre iniciar una partida carregant `config/example.yaml` per defecte o una ruta YAML explícita, i SHALL rebutjar una ruta inexistent o una configuració invàlida amb un error no ambigu.

#### Scenario: Default configuration starts a game
- **WHEN** l’usuari executa el CLI en mode de simulació sense indicar una configuració
- **THEN** el sistema carrega `config/example.yaml`, crea l’estat inicial i mostra equips, robots, objectius, ronda, fase i puntuacions

#### Scenario: Invalid configuration is reported
- **WHEN** l’usuari indica una ruta que no existeix o un YAML que no supera la validació
- **THEN** el CLI mostra l’error a stderr i acaba amb un codi de sortida diferent de zero

### Requirement: Execute a complete console simulation
El CLI SHALL oferir una seqüència de prova que avanci la partida mitjançant les accions públiques del motor i SHALL mostrar cada transició de fase, resultat de combat, puntuació i resultat final.

#### Scenario: Simulation reaches a terminal result
- **WHEN** l’usuari executa el mode de prova amb una configuració vàlida
- **THEN** la sortida mostra l’estat inicial, les transicions, els esdeveniments rellevants i un resultat final `team_a_wins`, `team_b_wins` o `draw`

#### Scenario: Terminal conditions are visible
- **WHEN** la simulació acaba perquè un equip arriba al llindar de victòria o perquè s’assoleix el límit de rondes
- **THEN** la sortida identifica explícitament la causa de tancament i les puntuacions finals

### Requirement: Support manual console actions
El CLI SHALL oferir un mode manual que accepti accions de l’usuari i SHALL delegar-ne la validació i l’execució al motor, mostrant els errors sense corrompre l’estat.

#### Scenario: Valid manual action advances the game
- **WHEN** l’usuari introdueix una acció vàlida per a la fase i l’equip actius
- **THEN** el CLI executa l’acció, mostra el resultat i imprimeix l’estat actualitzat

#### Scenario: Invalid manual action is rejected
- **WHEN** l’usuari introdueix una acció desconeguda, fora de fase o d’un equip inactiu
- **THEN** el CLI mostra l’error, conserva l’estat anterior i continua acceptant entrada

#### Scenario: Status shows robot positions
- **WHEN** l’usuari introdueix `status` durant una partida activa
- **THEN** la sortida inclou cada robot amb el seu identificador, equip, posició `(q,r)` i si està destruït

### Requirement: Make console runs reproducible
El CLI SHALL acceptar una llavor opcional i SHALL conservar-la en l’estat de partida perquè les execucions equivalents produeixin els mateixos esdeveniments aleatoris i resultats.

#### Scenario: Same seed produces same output
- **WHEN** dues execucions equivalents utilitzen la mateixa configuració, mode i llavor
- **THEN** les tirades de combat, els resums i el resultat final són idèntics

#### Scenario: Seed is shown in the run
- **WHEN** l’usuari proporciona una llavor
- **THEN** la sortida inicial identifica la llavor utilitzada

### Requirement: Keep console concerns outside the game engine
La interfície de consola SHALL consultar i executar l’estat mitjançant les API del motor i SHALL no duplicar regles de moviment, visibilitat, combat, puntuació o final de partida.

#### Scenario: Console delegates game resolution
- **WHEN** la consola executa una acció de moviment, dispar o final de fase
- **THEN** la validació i el resultat provenen del motor i la consola només els presenta
