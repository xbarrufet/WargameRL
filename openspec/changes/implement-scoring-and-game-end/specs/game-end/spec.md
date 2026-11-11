# Spec Delta

## Purpose

Aquesta capacitat determina el tancament de la partida de manera determinista,
incloent la victòria per punts, el límit de rondes i els resultats empatats.

## ADDED Requirements

### Requirement: End the game at the victory threshold
El sistema SHALL activar el final quan un equip arriba a `victory_points` i SHALL permetre completar el torn de l’altre equip si la puntuació s’assoleix durant el primer torn de la ronda.

#### Scenario: First team reaches threshold
- **WHEN** el primer equip de la ronda arriba a `victory_points` durant la puntuació
- **THEN** la partida queda pendent de completar el torn del segon equip

#### Scenario: Second team completes threshold round
- **WHEN** el segon equip finalitza el seu torn després que el primer hagi assolit el llindar
- **THEN** la partida acaba amb el resultat determinat per les puntuacions finals

#### Scenario: Team reaches threshold on second turn
- **WHEN** el segon equip de la ronda arriba a `victory_points` i el primer ja ha completat el seu torn
- **THEN** la partida acaba després d’aquest torn

### Requirement: Enforce the maximum round limit
El sistema SHALL acabar la partida en arribar al final de la ronda 15 si cap equip ha guanyat abans.

#### Scenario: Fifteenth round ends the game
- **WHEN** el segon equip finalitza `SCORING` de la ronda 15 sense una victòria anticipada
- **THEN** la partida acaba i es comparen les puntuacions

### Requirement: Determine the final result
El sistema SHALL assignar `TEAM_A_WINS`, `TEAM_B_WINS` o `DRAW` segons quina puntuació final sigui més alta.

#### Scenario: Team A has more points
- **WHEN** la partida acaba i l’equip A té més punts
- **THEN** el resultat és `TEAM_A_WINS`

#### Scenario: Team B has more points
- **WHEN** la partida acaba i l’equip B té més punts
- **THEN** el resultat és `TEAM_B_WINS`

#### Scenario: Final scores are tied
- **WHEN** la partida acaba i les puntuacions són iguals
- **THEN** el resultat és `DRAW`

### Requirement: Block actions after game end
El sistema SHALL rebutjar accions i transicions de fase quan el resultat ja no és `PENDING`.

#### Scenario: Finished game rejects action
- **WHEN** s’intenta executar una acció en una partida acabada
- **THEN** l’acció és rebutjada i l’estat final no canvia
