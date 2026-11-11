# game-state-model Specification

## Purpose
Aquesta capacitat defineix un estat de partida explícit, coherent i
serialitzable que serveix de frontera entre la configuració carregada i les
regles de joc futures.

## Requirements

### Requirement: Represent the board and coordinates
El sistema SHALL representar el tauler, les seves dimensions, les elevacions i les posicions amb coordenades hexagonals `q,r` enteres.

#### Scenario: Board created from configuration
- **WHEN** es crea l’estat inicial a partir d’una configuració vàlida
- **THEN** el tauler conserva les dimensions i totes les elevacions definides al YAML

#### Scenario: Coordinate preserves values
- **WHEN** es crea una posició amb `q` i `r`
- **THEN** la serialització conserva exactament els dos valors

### Requirement: Represent directions and phases
El sistema SHALL representar les sis orientacions `N`, `NE`, `SE`, `S`, `SW`, `NW` i les fases `MOVEMENT`, `SHOOTING`, `SCORING`.

#### Scenario: Valid direction is represented
- **WHEN** un robot es carrega amb una orientació vàlida
- **THEN** l’estat conserva aquesta orientació com una direcció del model

#### Scenario: Initial phase is movement
- **WHEN** es crea una partida nova
- **THEN** la fase inicial és `MOVEMENT`

### Requirement: Represent teams, robots and objectives
El sistema SHALL representar equips, robots i objectius amb els identificadors, propietats i posicions de la configuració validada.

#### Scenario: Entities are created from YAML
- **WHEN** es crea un estat a partir de `config/example.yaml`
- **THEN** tots els equips, robots i objectius del YAML apareixen a l’estat amb les seves dades

#### Scenario: Robot starts active and undamaged
- **WHEN** es crea un robot nou
- **THEN** té zero impactes acumulats i no està destruït

#### Scenario: Robot may occupy an objective
- **WHEN** un robot i un objectiu comparteixen una coordenada
- **THEN** l’estat és vàlid perquè l’objectiu no ocupa físicament la casella

### Requirement: Represent the complete game state
El sistema SHALL mantenir l’equip actiu, ronda, torn, fase, puntuacions, resultat, llavor opcional i el registre de si cada robot ja ha disparat en el torn actual dins de l’estat global.

#### Scenario: New game has deterministic initial state
- **WHEN** es crea una partida sense llavor
- **THEN** l’equip actiu és el primer equip, la ronda i el torn comencen a `1`, les puntuacions són zero, el resultat és pendent i cap robot consta com a disparat

#### Scenario: Seed is preserved
- **WHEN** es crea una partida amb una llavor explícita
- **THEN** la llavor queda disponible a l’estat per a la reproducció futura

#### Scenario: Shot tracking survives state round trip
- **WHEN** un robot dispara i l’estat es serialitza i es restaura dins del mateix torn
- **THEN** el robot continua constando com a disparat i no pot disparar una segona vegada

### Requirement: Create state only from validated configuration
El sistema SHALL construir un estat inicial únicament a partir d’una configuració que ja hagi superat la validació de la fase 1.

#### Scenario: Valid configuration creates state
- **WHEN** es passa una configuració vàlida al constructor de partida
- **THEN** es retorna un `GameState` complet sense modificar la configuració d’origen

#### Scenario: Invalid source is rejected
- **WHEN** la configuració no conté les dades necessàries per construir l’estat
- **THEN** la creació falla amb un error explicatiu i no retorna un estat parcial

### Requirement: Serialize and restore the game state
El sistema SHALL serialitzar i restaurar l’estat complet, inclosos els impactes, la destrucció i el registre de dispars, en una estructura determinista amb només dades primitives i col·leccions JSON-compatibles.

#### Scenario: Round trip preserves state
- **WHEN** un estat es serialitza i es torna a carregar
- **THEN** el nou estat és equivalent en tauler, entitats, dany, destrucció, dispars, fase, torn, puntuacions, resultat i llavor

#### Scenario: Serialized output is inspectable
- **WHEN** es serialitza un estat
- **THEN** la sortida no conté objectes de Pygame ni dependències de la interfície gràfica
