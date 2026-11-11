# Design

## Context

La línia de visió ja exposa una consulta pura (`assess_target`) que classifica
l’arc, el rang i el bloqueig per elevació. `GameState` conserva els robots,
les regles configurades i la llavor, mentre que el cicle de torn valida la
fase i l’equip però encara no disposa d’una acció de dispar ni d’un registre per
robot. Vegeu `proposal.md` i les delta specs per al contracte observable.

## Goals / Non-Goals

**Goals:**

- Afegir una resolució de combat atòmica i independent de Pygame.
- Fer explícits els resultats de totes les tirades per facilitar proves,
  depuració i reproducció.
- Integrar dany, destrucció i punts amb l’estat existent i la configuració.
- Reiniciar el registre de dispars en començar el torn de cada equip.

**Non-Goals:**

- No canviar la geometria o les regles de visibilitat ja especificades.
- No afegir cobertura, armes alternatives, crítics ni efectes d’estat.
- No implementar encara puntuació d’objectius, final de partida o UI.

## Decisions

- **Acció i resolució separades:** `ShootAction` contindrà la intenció
  (`attacker_id`, `target_id`) i una funció/mòdul de regles farà la resolució.
  Això manté el motor com a font de veritat i permet provar la resolució sense
  interfície.
- **RNG injectable i llavor de partida:** la resolució rebrà un generador
  controlat pel motor; si només es disposa de `GameState.seed`, es crearà un
  flux determinista associat a l’estat. No es faran crides directes a l’atzar
  global, perquè dificulten el replay.
- **Traça immutable del resultat:** el resultat inclourà tirada d’impacte,
  modificador, èxit, tirades de salvació, armadura aplicada, impactes causats,
  impactes totals i destrucció. Els errors de validació es produiran abans de
  mutar l’estat.
- **Dany al model, punts al compte de l’atacant:** el robot defensor acumula
  impactes i queda marcat destruït en arribar al màxim. Els punts s’afegeixen
  una sola vegada en la mateixa transició de destrucció; un robot destruït no
  es torna a validar com a blanc.
- **Seguiment per torn:** el registre de robots que han disparat viu a
  `GameState` i es buida en la transició a `MOVEMENT` del torn següent. Es
  serialitza per impedir dobles dispars després d’un round trip.
- **Arc defensiu des de la geometria existent:** es reutilitza la relació
  retornada per visibilitat per escollir `front`, `side` o `rear`; no es
  duplica la classificació dins del combat.

## Risks / Trade-offs

- [Risk] Un RNG persistent pot fer que el resultat depengui de l’ordre de les
  accions → Mitigació: conservar l’estat del generador o consumir-lo només en
  resolucions acceptades i cobrir replays amb proves de llavor.
- [Risk] El registre de dispars pot quedar desfasat en transicions existents
  → Mitigació: centralitzar el reset en el canvi de torn i provar les dues
  transicions d’equip.
- [Risk] La retirada física del robot pot trencar consultes que recorren tots
  els robots → Mitigació: conservar l’entitat marcada com a destruïda, ignorar-la
  en ocupació, blancs i puntuació, i validar-ho amb regressions.

## Migration Plan

Afegir els camps nous amb valors inicials buits/zero per als estats creats de
nou i fer que `from_dict` accepti només el contracte serialitzat actualitzat
segons el patró estricte del projecte. Actualitzar `config/example.yaml` i les
proves; no cal migració de dades persistents fora dels round trips de tests.
Si la integració falla, es pot revertir el canvi de combat sense modificar la
configuració de les fases anteriors.
