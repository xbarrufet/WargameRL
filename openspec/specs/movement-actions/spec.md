# movement-actions Specification

## Purpose

Aquesta capacitat permet al motor validar i executar el moviment dels robots
segons les regles de moviment normal, pivot i salt de WargameRL.

## Requirements

### Requirement: Execute normal movement
El sistema SHALL permetre avançar només en la direcció d'encarament, amb un cost d'un punt per casella, sense superar `M` punts i sense travessar robots no destruïts.

#### Scenario: Advance on valid terrain
- **WHEN** un robot avança cap a una casella lliure de la mateixa elevació o inferior dins del pressupost
- **THEN** la seva posició s'actualitza i el cost consumit és un punt per casella

#### Scenario: Reject blocked or higher terrain
- **WHEN** una ruta normal travessa un robot o intenta entrar en una casella d'elevació superior
- **THEN** l'acció és rebutjada i l'estat del robot no canvia

### Requirement: Combine pivots and advances
El sistema SHALL permetre combinar pivots de 60° i avanços dins del pressupost de moviment del robot.

#### Scenario: Pivot and advance within budget
- **WHEN** la seqüència de pivots i avanços té un cost total menor o igual que `M`
- **THEN** el motor l'executa en ordre i conserva l'orientació i posició finals

#### Scenario: Stop before exhausting movement
- **WHEN** un robot executa menys accions que el seu pressupost màxim
- **THEN** l'acció és vàlida i el robot pot quedar-se a la seva casella actual

### Requirement: Execute jumping movement
El sistema SHALL permetre saltar fins a `J` hexàgons en qualsevol direcció i elevació, travessant robots durant la trajectòria però no ocupant-ne la casella final.

#### Scenario: Jump across terrain and robots
- **WHEN** el destí és dins del tauler, lliure i a distància menor o igual que `J`
- **THEN** el robot es mou al destí encara que la ruta travessi robots o elevacions diferents

#### Scenario: Reject invalid jump destination
- **WHEN** el destí és fora del tauler, ocupat o supera `J`
- **THEN** el salt és rebutjat i la posició del robot no canvia

### Requirement: Choose orientation after jump
El sistema SHALL permetre escollir lliurement l'orientació final del robot després d'un salt sense cost addicional.

#### Scenario: Free final orientation
- **WHEN** un salt vàlid especifica una de les sis orientacions permeses
- **THEN** el robot acaba amb aquella orientació i no consumeix punts addicionals per pivotar

### Requirement: Apply movement atomically
El sistema SHALL validar una acció completa abans de modificar la posició, orientació o estat de moviment del robot.

#### Scenario: Invalid sequence has no partial effects
- **WHEN** una seqüència conté una acció invàlida després d'una acció vàlida
- **THEN** tota la seqüència és rebutjada i l'estat original es conserva

### Requirement: Expose accessible movement destinations
El sistema SHALL poder retornar les destinacions accessibles segons el tipus de moviment i l'estat actual del tauler.

#### Scenario: Accessible destinations respect rules
- **WHEN** es consulten les destinacions d'un robot
- **THEN** el resultat exclou caselles fora del tauler, terreny invàlid, caselles ocupades com a destí i costos superiors al pressupost
