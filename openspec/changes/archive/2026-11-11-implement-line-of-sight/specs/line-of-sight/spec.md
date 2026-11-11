# Spec Delta

## Purpose

Aquesta capacitat determina de manera determinista els blancs visibles i
vàlids per a cada robot segons l’orientació, el rang i les elevacions del mapa.

## ADDED Requirements

### Requirement: Calculate the frontal arc
El sistema SHALL determinar un arc frontal de 120° i el seu arc posterior a partir de les sis orientacions hexagonals definides, amb els límits projectats pels costats esquerre i dret de l’encarament en flat-top.

#### Scenario: Front-facing target is classified
- **WHEN** un blanc es troba dins del sector frontal de l’orientació del robot
- **THEN** el blanc es classifica com a frontal i pot continuar la validació de visibilitat

#### Scenario: Side and rear targets are classified
- **WHEN** un blanc es troba fora de l’arc frontal
- **THEN** es classifica com a lateral o posterior segons el sector corresponent

#### Scenario: Flat-top arc boundaries
- **WHEN** es consulta l’arc d’un robot en un mapa flat-top
- **THEN** el sector frontal de 120° queda delimitat per la projecció dels costats esquerre i dret de l’encarament, segons `docs/arc_frontal.png`

### Requirement: Enforce weapon range
El sistema SHALL rebutjar blancs que superin el rang `R` del robot atacant.

#### Scenario: Target within range
- **WHEN** la distància hexagonal al blanc és menor o igual que `R`
- **THEN** el rang es considera vàlid

#### Scenario: Target beyond range
- **WHEN** la distància hexagonal al blanc és superior a `R`
- **THEN** el blanc és rebutjat amb un motiu que identifica el rang excedit

### Requirement: Resolve elevation line of sight
El sistema SHALL bloquejar la línia de visió entre posicions baixes quan una elevació alta queda interposada, i SHALL permetre que una posició alta vegi per sobre del terreny elevat.

#### Scenario: High terrain blocks low targets
- **WHEN** l’atacant i el blanc són en elevació baixa i una casella alta queda interposada
- **THEN** el blanc és rebutjat per bloqueig d’elevació

#### Scenario: Elevated attacker sees over terrain
- **WHEN** l’atacant és en elevació alta i el blanc compleix l’arc i el rang
- **THEN** el terreny elevat interposat no bloqueja el blanc

### Requirement: Ignore robots as line of sight obstacles
El sistema SHALL ignorar els robots interposats en calcular la línia de visió.

#### Scenario: Robot between attacker and target
- **WHEN** un altre robot ocupa una casella de la línia entre l’atacant i el blanc
- **THEN** el robot interposat no bloqueja la visibilitat

### Requirement: Expose valid targets and rejection reasons
El sistema SHALL retornar els blancs vàlids i un motiu determinista per a cada blanc rebutjat per arc, rang, elevació o estat invàlid.

#### Scenario: Valid target is returned
- **WHEN** un robot enemic compleix l’arc frontal, el rang i la línia de visió
- **THEN** apareix a la llista de blancs vàlids

#### Scenario: Invalid target has an explanation
- **WHEN** un blanc falla una comprovació de visibilitat
- **THEN** no apareix entre els blancs vàlids i el resultat identifica la comprovació que ha fallat
