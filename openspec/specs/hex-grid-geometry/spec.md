# hex-grid-geometry Specification

## Purpose

Aquesta capacitat proporciona una geometria hexagonal única i determinista per
al motor, les regles i la futura interfície visual de WargameRL.

## Requirements

### Requirement: Validate board coordinates
El sistema SHALL considerar vàlida una coordenada només quan `q` i `r` siguin enters dins de les dimensions del tauler.

#### Scenario: Coordinate inside board
- **WHEN** es consulta una coordenada amb `0 <= q < width` i `0 <= r < height`
- **THEN** la coordenada és acceptada

#### Scenario: Coordinate outside board
- **WHEN** `q` o `r` queda fora dels límits del tauler
- **THEN** la consulta falla amb un error que identifica la coordenada i el límit infringit

### Requirement: Calculate hex neighbors and distance
El sistema SHALL calcular els sis veïns axials i la distància hexagonal segons la convenció `q,r` del tauler.

#### Scenario: Six neighbors
- **WHEN** es demanen els veïns d’una casella interior
- **THEN** es retornen exactament les sis coordenades axials adjacents

#### Scenario: Board edge neighbors
- **WHEN** es demanen els veïns d’una casella del límit
- **THEN** només es retornen veïns dins del tauler

#### Scenario: Hex distance
- **WHEN** es calcula la distància entre dues coordenades
- **THEN** el resultat és zero per a la mateixa casella i correspon al nombre mínim de passos entre hexàgons

### Requirement: Query elevation and occupancy
El sistema SHALL permetre consultar l’elevació i si una casella està ocupada sense modificar l’estat de la partida.

#### Scenario: Elevation lookup
- **WHEN** es consulta una coordenada vàlida
- **THEN** es retorna l’elevació `0` o `1` definida al mapa

#### Scenario: Occupied cell lookup
- **WHEN** una entitat ocupa una coordenada
- **THEN** la consulta d’ocupació identifica l’entitat i una casella lliure es retorna com no ocupada

### Requirement: Convert flat-top coordinates to screen positions
El sistema SHALL convertir coordenades `q,r` a píxels utilitzant hexàgons flat-top, una mida positiva i un origen explícit, sense dependre de Pygame.

#### Scenario: Coordinate projection
- **WHEN** es projecta una coordenada amb una mida i origen vàlids
- **THEN** es retorna el centre de píxels corresponent a la fórmula flat-top documentada

#### Scenario: Invalid projection size
- **WHEN** la mida de l’hexàgon és zero o negativa
- **THEN** la conversió falla amb un error de paràmetre

### Requirement: Convert screen positions to board coordinates
El sistema SHALL convertir una posició de pantalla a la coordenada flat-top que conté el punt i rebutjar punts fora del tauler.

#### Scenario: Point inside hexagon
- **WHEN** el punt de pantalla cau dins d’un hexàgon del tauler
- **THEN** es retorna la coordenada d’aquell hexàgon

#### Scenario: Point outside board
- **WHEN** el punt queda fora de tots els hexàgons del tauler
- **THEN** la conversió retorna absència de coordenada o un error explícit de punt fora del tauler, segons l’API escollida
