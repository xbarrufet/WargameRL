# pygame-visualization Specification

## Purpose

Aquesta capacitat proporciona una interfície Pygame interactiva que visualitza l’estat de la partida i executa accions a través del motor, mantenint la separació entre presentació i regles.

## Requirements

### Requirement: Render the current game state

La UI SHALL mostrar el tauler hexagonal, les elevacions, les zones, els objectius, els robots, les seves orientacions i l’estat general de la partida.

#### Scenario: Initial game is visible
- **WHEN** s’inicia la UI amb una configuració vàlida
- **THEN** la finestra mostra el mapa, les entitats, la fase, l’equip actiu, la ronda i les puntuacions

#### Scenario: State changes are reflected
- **WHEN** el motor accepta una acció vàlida
- **THEN** la UI redibuixa la posició, orientació, dany, puntuació o fase actualitzats sense mantenir una còpia divergent de l’estat

### Requirement: Use configured sprites and geometry

La UI SHALL carregar els sprites configurats i convertir les coordenades del motor a píxels segons la geometria hexagonal establerta.

#### Scenario: Configured sprite is rendered
- **WHEN** un equip té un sprite PNG vàlid a la configuració
- **THEN** els robots d’aquest equip es mostren amb el sprite corresponent i la seva orientació és visible

#### Scenario: Board coordinates map consistently
- **WHEN** una casella del tauler es renderitza o se selecciona
- **THEN** la conversió entre coordenada `q,r` i posició de pantalla és coherent amb la convenció flat-top del motor

### Requirement: Select entities and cells

La UI SHALL permetre seleccionar robots i caselles amb el ratolí i SHALL indicar visualment la selecció actual.

#### Scenario: Robot is selected
- **WHEN** l’usuari fa clic sobre un robot seleccionable de l’equip actiu
- **THEN** el robot queda ressaltat i la UI mostra les opcions o consultes disponibles per a la fase actual

#### Scenario: Cell is selected
- **WHEN** l’usuari fa clic sobre una casella del mapa
- **THEN** la UI identifica la coordenada seleccionada i la fa servir per a l’acció compatible actual

### Requirement: Highlight engine-provided options

La UI SHALL ressaltar només les destinacions de moviment, salts i blancs vàlids retornats pel motor.

#### Scenario: Movement options are highlighted
- **WHEN** hi ha un robot seleccionat durant `MOVEMENT`
- **THEN** la UI ressalta les destinacions accessibles segons la consulta del motor

#### Scenario: Valid targets are highlighted
- **WHEN** hi ha un robot seleccionat durant `SHOOTING`
- **THEN** la UI ressalta els blancs vàlids retornats pel motor i no presenta com a vàlids els blancs rebutjats

### Requirement: Delegate user actions to the engine

La UI SHALL construir i enviar accions públiques al motor, i SHALL mostrar els errors de validació sense modificar directament l’estat del joc.

#### Scenario: Valid action is executed
- **WHEN** l’usuari confirma una acció compatible amb la fase actual
- **THEN** el motor la valida i executa, i la UI mostra el nou estat o el resultat de combat

#### Scenario: Invalid action is reported
- **WHEN** el motor rebutja una acció sol·licitada des de la UI
- **THEN** la UI mostra el missatge d’error, conserva la selecció útil i no altera l’estat

### Requirement: Present terminal game results

La UI SHALL indicar la causa del final de partida i mostrar el guanyador o l’empat amb les puntuacions finals.

#### Scenario: Team wins
- **WHEN** el motor arriba a un resultat `team_a_wins` o `team_b_wins`
- **THEN** la UI mostra el resultat final, la causa de tancament i les puntuacions

#### Scenario: Game is a draw
- **WHEN** el motor arriba a un resultat `draw`
- **THEN** la UI mostra explícitament l’empat i les puntuacions finals

### Requirement: Keep graphical concerns outside the engine

La UI SHALL dependre de les API del motor i SHALL funcionar com a client, sense implementar regles alternatives de moviment, visibilitat, combat, puntuació o final de partida.

#### Scenario: UI uses engine resolution
- **WHEN** l’usuari interactua amb el mapa
- **THEN** tota validació i resolució observable prové del motor i la UI només presenta consultes, accions i resultats
