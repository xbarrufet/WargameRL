# Spec Delta

## Purpose

Aquesta capacitat segueix `docs/GAME_RULES.md` per definir el nou moviment de
córrer i saltar i la resolució dels impactes, incloent els paràmetres `J` i `H`
configurables per robot.

## ADDED Requirements

### Requirement: Configure global game parameters
La configuració SHALL permetre els valors globals definitius: radi de control d’objectius `2`, distància mínima entre objectius `5`, vida màxima `5`, punts per destrucció `3`, punts per victòria `15` i punts d’objectiu `1/3/5`.

#### Scenario: Definitive parameters are loaded
- **WHEN** es carrega la configuració d’exemple actualitzada
- **THEN** el model conserva els valors globals definits per aquesta revisió

#### Scenario: Objective spacing is valid
- **WHEN** dos objectius estan més a prop que la distància mínima configurada
- **THEN** la configuració es rebutja indicant les posicions conflictives

### Requirement: Configure robot movement and hit values
Cada robot SHALL tenir `movement` (`M`), `jump` (`J`) i `hit_target` (`H`) com enters positius, a més de rang i dany.

#### Scenario: Robot values load from YAML
- **WHEN** es carrega una configuració amb els tres valors
- **THEN** `M`, `J` i `H` queden disponibles al robot i es conserven en serialitzar-lo; l’exemple usa `M=3`, `J=4` i `H=4+`

#### Scenario: Missing or invalid value is rejected
- **WHEN** falta `jump` o `hit_target`, o un dels valors no és positiu
- **THEN** la configuració es rebutja identificant el camp afectat

### Requirement: Preserve unresolved rule decisions
La implementació SHALL deixar bloquejades les decisions que `docs/GAME_RULES.md` marca com pendents fins que siguin definides explícitament.

#### Scenario: Pending geometry is not guessed
- **WHEN** la implementació necessita una decisió no definida a `docs/GAME_RULES.md`
- **THEN** el canvi es pausa i demana una decisió explícita

### Requirement: Resolve running movement
El moviment de córrer SHALL permetre avançar fins a `M` caselles cap endavant, només per caselles de la mateixa elevació o inferior, combinant pivots i sense travessar robots.

#### Scenario: Run respects movement and terrain
- **WHEN** un robot corre durant la fase de moviment
- **THEN** només pot ocupar una ruta cap endavant de com a màxim `M` caselles vàlides segons l’elevació i l’ocupació

### Requirement: Resolve jumping movement
El moviment de saltar SHALL permetre avançar fins a `J` caselles en qualsevol direcció i elevació, travessar robots i acabar amb una orientació triada, però no acabar en una casella ocupada.

#### Scenario: Jump crosses elevation and robots
- **WHEN** un robot executa un salt vàlid
- **THEN** pot travessar elevacions i robots, però el destí final ha d’estar lliure i dins del mapa

### Requirement: Resolve shooting hit chance
El dispar SHALL tirar `1D6` i impactar només quan el resultat més els modificadors sigui almenys `H`, després de comprovar línia de visió i rang.

#### Scenario: Stationary shooter gets bonus
- **WHEN** el robot no ha mogut abans de disparar
- **THEN** la tirada d’impacte rep `+1`

#### Scenario: Jumping shooter gets penalty
- **WHEN** el robot ha saltat abans de disparar
- **THEN** la tirada d’impacte rep `-2`

### Requirement: Remove elevation cover bonus
El sistema SHALL no aplicar cap bonificació de cobertura per estar el blanc en una elevació superior.

#### Scenario: Elevated target has no cover bonus
- **WHEN** un robot dispara a un blanc d’elevació superior
- **THEN** la tirada d’armadura no rep cap modificador per elevació
