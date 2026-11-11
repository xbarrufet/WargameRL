# Spec Delta

## ADDED Requirements

### Requirement: Resolve objective control
El sistema SHALL determinar el controlador d’un objectiu comptant robots no destruïts de cada equip dins de `objective_radius`; l’empat no atorga control.

#### Scenario: Team controls objective by majority
- **WHEN** un equip té més robots dins del radi que l’altre
- **THEN** aquest equip controla l’objectiu

#### Scenario: Tied objective has no controller
- **WHEN** els dos equips tenen el mateix nombre de robots dins del radi
- **THEN** l’objectiu no té controlador i no genera punts

#### Scenario: Destroyed robots do not contribute
- **WHEN** un robot destruït és dins del radi d’un objectiu
- **THEN** no compta per determinar el control

### Requirement: Score controlled objectives once per turn
El sistema SHALL puntuar només l’equip actiu al final del seu torn i com a màxim una vegada cada objectiu durant aquell torn.

#### Scenario: Active team scores controlled objective
- **WHEN** l’equip actiu controla un objectiu durant `SCORING`
- **THEN** rep el valor configurat segons la zona de l’objectiu

#### Scenario: Inactive team does not score
- **WHEN** un objectiu està controlat per l’equip no actiu durant `SCORING`
- **THEN** no s’afegeixen punts a l’equip no actiu

#### Scenario: Objective can score in consecutive turns
- **WHEN** el mateix equip continua controlant un objectiu en torns consecutius
- **THEN** l’objectiu torna a generar els seus punts en cada torn
