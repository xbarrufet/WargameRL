# Spec Delta

## MODIFIED Requirements

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

### Requirement: Serialize and restore the game state
El sistema SHALL serialitzar i restaurar l’estat complet, inclosos els impactes, la destrucció i el registre de dispars, en una estructura determinista amb només dades primitives i col·leccions JSON-compatibles.

#### Scenario: Round trip preserves state
- **WHEN** un estat es serialitza i es torna a carregar
- **THEN** el nou estat és equivalent en tauler, entitats, dany, destrucció, dispars, fase, torn, puntuacions, resultat i llavor

#### Scenario: Serialized output is inspectable
- **WHEN** es serialitza un estat
- **THEN** la sortida no conté objectes de Pygame ni dependències de la interfície gràfica
