# Design

## Context

La configuració actual només modela `movement`, `range` i `damage`, mentre que
`docs/GAME_RULES.md` ja defineix `J` i `H`. El model i el carregador han de
reflectir aquesta font normativa abans d’implementar les accions de moviment i
combat. `AGENTS.md` exigeix consultar aquestes regles abans de modificar
mecàniques.

Els paràmetres globals definitius d’aquesta revisió són: radi de control dels
objectius `2`, distància mínima entre objectius `5`, vida màxima dels robots `5`
impactes, `3` punts per destrucció, `15` punts per victòria i punts d’objectiu
`1/3/5` per zona amiga, neutral i enemiga.

Els valors inicials de cada robot són `movement: 3`, `jump: 4` i
`hit_target: 4`, on `H=4` significa impactar amb un resultat de 4 o més.

## Goals / Non-Goals

**Goals:**

- Fer explícits `jump` i `hit_target` en totes les capes del
  model.
- Separar la resolució de córrer, saltar i impactar en regles testables.
- Fer que la línia de visió i el combat no introdueixin cobertura per elevació.
- Mantenir el motor independent de Pygame.

**Non-Goals:**

- Implementar encara el cicle complet de torns.
- Resoldre puntuació, final de partida o entrenament RL.
- Canviar les regles d’armadura frontal, lateral i posterior.

## Decisions

- **Noms del contracte funcional:** `jump` i `hit_target` són els noms
  establerts a `docs/GAME_RULES.md` i s’han de respectar al YAML i al model.
- **Camps obligatoris:** la configuració estricta evita robots amb regles de
  salt o impacte implícites.
- **Modificadors de tirada separats de `H`:** `H` és la dificultat base i els
  estats de moviment s’apliquen com a modificadors en el moment de disparar.
- **Cobertura eliminada del càlcul:** l’elevació encara pot afectar la línia de
  visió, però no modifica la tirada d’armadura.

## Risks / Trade-offs

- [Risk] El canvi trenca YAML existents → actualitzar l’exemple i reportar el
  camp exacte en els errors de càrrega.
- [Risk] El dispar depèn de l’estat de moviment anterior → l’estat de la fase
  de moviment haurà de conservar si el robot ha corregut o saltat.

## Migration Plan

Afegir `jump: 4` i `hit_target: 4` a tots els robots existents.

La implementació s’ha d’aturar abans de fixar la geometria dels arcs, el
traçat de línia de visió, el bloqueig per robots, la convenció exacta de
coordenades o el límit de rondes: `docs/GAME_RULES.md` els declara decisions
pendents i no es poden resoldre per suposició.
