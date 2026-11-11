# combat-resolution Specification

## Purpose

Aquesta capacitat resol de manera determinista i inspeccionable els dispars
dels robots, les salvacions, el dany, la destrucció i la recompensa associada.

## Requirements

### Requirement: Execute one valid shot
El sistema SHALL permetre que un robot actiu executi un dispar durant `SHOOTING` contra un robot enemic visible, frontal i dins del seu rang.

#### Scenario: Valid target is shot
- **WHEN** un robot actiu dispara durant `SHOOTING` contra un blanc enemic retornat com a visible
- **THEN** el sistema resol el combat i retorna un resum del resultat

#### Scenario: Invalid target is rejected
- **WHEN** el blanc és aliat, destruït, fora de l’arc, fora de rang o bloquejat per elevació
- **THEN** el dispar és rebutjat, l’estat no canvia i l’error identifica la causa

### Requirement: Apply movement modifier to hit roll
El sistema SHALL tirar `1D6` per impactar i considerar l’impacte reeixit quan el resultat més el modificador de moviment iguala o supera `H`.

#### Scenario: Stationary attacker gets bonus
- **WHEN** el robot no s’ha mogut durant el torn
- **THEN** la tirada d’impacte usa modificador `+1`

#### Scenario: Normal movement has no modifier
- **WHEN** el robot ha fet moviment normal durant el torn
- **THEN** la tirada d’impacte usa modificador `0`

#### Scenario: Jumping attacker is penalized
- **WHEN** el robot ha saltat durant el torn
- **THEN** la tirada d’impacte usa modificador `-2`

### Requirement: Resolve armor saves and damage
Si el dispar impacta, el sistema SHALL tirar `D` daus de salvació i causar un impacte per cada dau inferior al valor d’armadura de l’arc atacat.

#### Scenario: Failed saves cause damage
- **WHEN** un impacte produeix salvacions amb resultats per sota de l’armadura aplicable
- **THEN** el defensor acumula un impacte per cada salvació fallada

#### Scenario: Armor depends on target arc
- **WHEN** el blanc és atacat des del front, lateral o posterior
- **THEN** s’aplica respectivament l’armadura `front`, `side` o `rear` configurada

### Requirement: Destroy damaged robots and award points
El sistema SHALL marcar com a destruït i retirar del joc un robot que arribi a `robot_max_damage`, i SHALL concedir una sola vegada `robot_destruction_points` a l’equip que l’ha destruït.

#### Scenario: Damage destroys robot
- **WHEN** els impactes acumulats del defensor arriben al màxim configurat
- **THEN** el robot queda destruït, deixa d’ocupar el mapa i no pot executar accions

#### Scenario: Destruction points are awarded once
- **WHEN** un robot enemic és destruït per primera vegada
- **THEN** només l’equip atacant rep els punts configurats de destrucció

### Requirement: Reproduce combat with a seed
El sistema SHALL permetre controlar l’atzar amb una llavor perquè dues execucions equivalents produeixin les mateixes tirades i el mateix resum de combat.

#### Scenario: Same seed gives same result
- **WHEN** dues partides equivalents resolen el mateix dispar amb la mateixa llavor
- **THEN** les tirades d’impacte i salvació i el resultat són idèntics

#### Scenario: Combat summary exposes rolls
- **WHEN** es resol un dispar
- **THEN** el resum inclou la tirada d’impacte, el modificador, les salvacions i els impactes causats
