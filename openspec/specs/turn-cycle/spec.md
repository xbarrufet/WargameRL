# turn-cycle Specification

## Purpose

Aquesta capacitat coordina les fases i els torns d’equip de WargameRL perquè el
motor pugui avançar una partida de manera determinista i validable.

## Requirements

### Requirement: Advance through the turn phases
El sistema SHALL avançar les fases en l’ordre `MOVEMENT`, `SHOOTING`, `SCORING` quan l’equip actiu finalitza cada fase.

#### Scenario: Movement advances to shooting
- **WHEN** l’equip actiu executa una `EndPhaseAction` durant `MOVEMENT`
- **THEN** la fase passa a `SHOOTING` i l’equip actiu es conserva

#### Scenario: Shooting advances to scoring
- **WHEN** l’equip actiu executa una `EndPhaseAction` durant `SHOOTING`
- **THEN** la fase passa a `SCORING` i l’equip actiu es conserva

### Requirement: Change the active team after scoring
El sistema SHALL conservar les regles configurades com a `RulesConfig` immutable dins de l’estat i SHALL finalitzar `SCORING` aplicant-les a la puntuació de l’equip actiu abans de canviar a l’altre equip amb la fase `MOVEMENT`.

#### Scenario: First team completes its turn
- **WHEN** el primer equip finalitza `SCORING`
- **THEN** només aquest equip puntua, l’equip actiu canvia a l’altre i la fase torna a `MOVEMENT`

#### Scenario: Round advances after both teams
- **WHEN** el segon equip finalitza `SCORING`
- **THEN** només aquest equip puntua, l’equip actiu torna al primer equip, la fase torna a `MOVEMENT` i la ronda augmenta en un

#### Scenario: Rules survive state round trip
- **WHEN** un `GameState` amb regles configurades es serialitza i es restaura
- **THEN** el `RulesConfig` restaurat és equivalent a l’original i continua disponible per puntuar

### Requirement: Restrict actions to the active team and phase
El sistema SHALL rebutjar qualsevol acció d’un robot que no pertanyi a l’equip actiu, que no correspongui a la fase actual o que contradigui el límit d’una acció de dispar per robot i torn.

#### Scenario: Inactive team action is rejected
- **WHEN** un robot de l’equip no actiu intenta executar una acció
- **THEN** l’acció és rebutjada i l’estat de la partida no canvia

#### Scenario: Wrong phase action is rejected
- **WHEN** una acció de moviment, dispar o puntuació s’envia fora de la seva fase
- **THEN** l’acció és rebutjada i l’estat de la partida no canvia

#### Scenario: Robot cannot shoot twice in one turn
- **WHEN** un robot que ja ha disparat en el torn actual intenta disparar de nou
- **THEN** el segon dispar és rebutjat i l’estat no canvia

#### Scenario: Each robot can shoot once
- **WHEN** dos robots de l’equip actiu disparen una vegada durant la mateixa fase
- **THEN** tots dos dispars són vàlids si compleixen les regles del blanc

### Requirement: Preserve free robot order within a phase
El sistema SHALL permetre que els robots de l’equip actiu actuïn en qualsevol ordre dins de la fase corresponent.

#### Scenario: Robots act in arbitrary order
- **WHEN** dos robots de l’equip actiu actuen en ordre diferent dins de la mateixa fase
- **THEN** totes dues seqüències són vàlides si les seves accions individuals compleixen les regles de la fase

### Requirement: End phases explicitly
El sistema SHALL exposar una `EndPhaseAction` que finalitzi la fase actual sense permetre saltar-se fases ni executar transicions implícites.

#### Scenario: End phase uses current state
- **WHEN** es valida una `EndPhaseAction` en una fase vàlida
- **THEN** només s’aplica la transició definida per la fase actual i l’estat resultant és coherent
