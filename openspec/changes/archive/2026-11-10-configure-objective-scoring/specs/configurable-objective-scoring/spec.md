# Spec Delta

## Purpose

Aquesta capacitat permet definir al YAML quants punts aporta cada tipus de
zona d’objectiu i evita codificar els valors de puntuació dins del motor.

## ADDED Requirements

### Requirement: Configure objective points by zone relation
La configuració SHALL incloure punts enters no negatius per a zones `friendly`, `neutral` i `enemy`, interpretades respecte de l’equip que puntua.

#### Scenario: Default example values are loaded
- **WHEN** es carrega `config/example.yaml`
- **THEN** els punts carregats són `friendly: 1`, `neutral: 3` i `enemy: 5`

#### Scenario: Custom objective values are loaded
- **WHEN** una configuració defineix valors diferents per a les tres zones
- **THEN** la configuració interna conserva exactament aquests valors

### Requirement: Validate objective point configuration
El sistema SHALL rebutjar si falta alguna de les tres claus de punts o si un valor no és un enter no negatiu.

#### Scenario: Missing point category
- **WHEN** falta `friendly`, `neutral` o `enemy`
- **THEN** la càrrega falla i identifica la clau absent

#### Scenario: Invalid point value
- **WHEN** un valor de punts és decimal, text o negatiu
- **THEN** la càrrega falla i identifica el valor afectat

### Requirement: Use configured points for scoring
Les regles SHALL calcular els punts d’un objectiu segons la relació de la seva zona amb l’equip que puntua: `friendly`, `neutral` o `enemy`.

#### Scenario: Team scores its own zone
- **WHEN** un equip puntua un objectiu de la seva zona
- **THEN** rep el valor configurat com `friendly`

#### Scenario: Team scores neutral or enemy zone
- **WHEN** un equip puntua un objectiu neutral o de la zona de l’altre equip
- **THEN** rep respectivament els valors configurats com `neutral` o `enemy`

### Requirement: Keep functional rules as the source of truth
La documentació tècnica SHALL referenciar els valors i la semàntica de `DESCRIPCIO.md` sense definir una regla funcional alternativa.

#### Scenario: Documentation has one scoring definition
- **WHEN** es consulta la documentació funcional i tècnica
- **THEN** totes dues descriuen els valors `1/3/5` i no presenten valors contradictoris
