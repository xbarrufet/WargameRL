# Spec Delta

## MODIFIED Requirements

### Requirement: Restrict actions to the active team and phase
El sistema SHALL rebutjar qualsevol acció d’un robot que no pertanyi a l’equip actiu, que no correspongui a la fase actual o que contradigui el límit d’una acció de dispar per robot i torn.

#### Scenario: Inactive team action is rejected
- **WHEN** un robot de l’equip no actiu intenta executar una acció
- **THEN** l’acció és rebutjada i l’estat de la partida no canvia

#### Scenario: Wrong phase action is rejected
- **WHEN** una acció de moviment, dispar o puntuació s’envia fora de la seva fase
- **THEN** l’acció és rebutjada i l’estat de la partida no canvia

#### Scenario: Robot cannot shoot twice in one turn
- **WHEN** un robot que ja ha disparat en el torn actual intenta disparar de nou
- **THEN** el segon dispar és rebutjat i l’estat no canvia

#### Scenario: Each robot can shoot once
- **WHEN** dos robots de l’equip actiu disparen una vegada durant la mateixa fase
- **THEN** tots dos dispars són vàlids si compleixen les regles del blanc

