# yaml-configuration Specification

## Purpose
Aquesta capacitat defineix com una configuració YAML de WargameRL es converteix
en una configuració interna segura abans d’iniciar una partida.

## Requirements

### Requirement: Load a valid game configuration
El sistema SHALL carregar una configuració YAML vàlida i retornar la seva configuració interna amb mapa, objectius, equips, robots i regles.

#### Scenario: Example configuration loads
- **WHEN** es carrega `config/example.yaml`
- **THEN** es retorna una configuració amb mapa de 17 × 15, dos equips i sis objectius

### Requirement: Enforce the supported schema
El sistema SHALL acceptar únicament configuracions amb `schema_version` enter igual a `1` i rebutjar camps desconeguts o camps obligatoris absents.

#### Scenario: Unsupported schema version
- **WHEN** la configuració declara una versió diferent de `1`
- **THEN** la càrrega falla amb un error que identifica `schema_version`

#### Scenario: Unknown field
- **WHEN** un objecte YAML conté un camp no definit per l’esquema
- **THEN** la càrrega falla i identifica els camps desconeguts

### Requirement: Validate the map and positions
El sistema SHALL validar que el mapa tingui 17 columnes, 15 files, elevacions `0` o `1` i que totes les coordenades siguin dins del mapa.

#### Scenario: Invalid elevation matrix
- **WHEN** una fila no té 17 valors o una elevació no és `0` ni `1`
- **THEN** la càrrega falla i identifica la fila i la columna afectades

#### Scenario: Out-of-bounds coordinate
- **WHEN** un objectiu o robot té una coordenada fora del mapa
- **THEN** la càrrega falla i identifica el camp de posició

### Requirement: Validate entities and gameplay configuration
El sistema SHALL validar identificadors únics, exactament dos equips, zones i orientacions vàlides, valors positius, robots no superposats entre ells i objectius no superposats entre ells.

#### Scenario: Duplicate identifiers or physical overlaps
- **WHEN** dos elements comparteixen identificador, o dos robots o dos objectius comparteixen posició
- **THEN** la càrrega falla abans de crear la configuració interna

#### Scenario: Robot may occupy an objective
- **WHEN** un robot i un objectiu comparteixen una posició
- **THEN** la configuració és vàlida perquè l’objectiu no ocupa físicament la casella

#### Scenario: Invalid robot or rule value
- **WHEN** un moviment, rang, dany o paràmetre de regla no és un enter positiu, o una orientació no està permesa
- **THEN** la càrrega falla i identifica el camp afectat

### Requirement: Resolve and validate team sprites
El sistema SHALL resoldre els sprites relatius al directori del fitxer YAML i exigir que cada sprite existeixi i tingui format PNG vàlid.

#### Scenario: Portable sprite paths
- **WHEN** el YAML i el directori `imgs/` es mouen conjuntament
- **THEN** les rutes dels sprites es resolen respecte del YAML carregat

#### Scenario: Missing or invalid sprite
- **WHEN** falta el sprite o el fitxer no és un PNG vàlid
- **THEN** la càrrega falla i identifica el camp `sprite` de l’equip

### Requirement: Report configuration errors
El sistema SHALL rebutjar una configuració invàlida amb una excepció específica que inclogui el camp o la ruta de dades afectada quan sigui aplicable.

#### Scenario: Invalid configuration is rejected
- **WHEN** qualsevol validació de l’esquema falla
- **THEN** no es retorna cap configuració parcial i l’error descriu la causa
