# Design

## Context

La configuració ja conserva `objective_radius`, `victory_points` i els punts
per zona, i `objective_points_for` resol la relació de zona. `execute_end_phase`
ja canvia de `SCORING` a `MOVEMENT`, però el càlcul actual només és parcial i
no actualitza `GameResult` ni aplica cap límit de rondes. Vegeu `proposal.md` i
les delta specs per al contracte observable.

## Goals / Non-Goals

**Goals:**

- Centralitzar el càlcul de control i puntuació en una operació determinista de
  `SCORING`.
- Fer explícit l’estat de final pendent quan el primer equip arriba al llindar
  i encara falta el torn del segon equip.
- Assignar el resultat final i bloquejar qualsevol mutació posterior.
- Mantenir la serialització compatible amb inspecció i round trips.

**Non-Goals:**

- No canviar els valors de punts configurables ni les regles de combat.
- No implementar encara la consola ni la UI.
- No afegir control parcial, bonificacions per elevació o desempats nous.

## Decisions

- **Control per recompte en temps de puntuació:** per cada objectiu es compten
  robots no destruïts dins del radi i només es puntua si l’equip actiu té una
  majoria estricta. No es mantindrà un controlador persistent, perquè la
  posició dels robots pot canviar abans de cada `SCORING`.
- **Puntuació idempotent per transició:** `SCORING` només s’executarà una
  vegada per la transició protegida per `EndPhaseAction`; els punts es calculen
  en aquell moment i no es tornen a aplicar per consultar l’estat.
- **Final en dos passos:** l’estat conservarà l’identificador de l’equip que
  ha assolit el llindar durant el primer torn de la ronda. Això permet deixar
  actuar el segon equip i tancar comparant les puntuacions després del seu
  `SCORING`. Si el llindar s’assoleix en el segon torn, es tanca immediatament.
- **Límit de ronda abans del següent torn:** després de puntuar el segon equip
  de la ronda 15, es calcula el resultat i no s’inicia una ronda 16.
- **Resultat únic i guardat:** `GameResult` passa de `PENDING` a un resultat
  final una sola vegada. Les validacions d’accions i transicions comprovaran
  aquest camp abans de modificar l’estat.
- **Regles de resultat generalitzables:** la comparació final usarà els
  identificadors reals dels dos equips per evitar codificar la victòria només
  amb noms, i maparà el resultat als enums existents `TEAM_A_WINS`,
  `TEAM_B_WINS` o `DRAW`.

## Risks / Trade-offs

- [Risk] El marcador de final pendent pot quedar inconsistent després d’un
  round trip → Mitigació: validar l’identificador, serialitzar-lo i provar la
  continuació exacta del torn posterior.
- [Risk] Un robot destruït pot continuar comptant si el càlcul recorre totes les
  entitats → Mitigació: filtrar explícitament `destroyed` i cobrir aquest cas.
- [Risk] El canvi de resultat pot afectar proves de torn existents → Mitigació:
  mantenir `PENDING` com a estat inicial i afegir regressions per transicions
  normals, victòria anticipada i ronda 15.

## Migration Plan

Afegir els camps d’estat necessaris amb valors inicials buits o `PENDING` i
incloure’ls en `to_dict`/`from_dict`. Les partides existents sense final
pendent continuaran com a partides actives. Actualitzar la documentació de la
fase 8 i executar tota la suite abans d’arxivar el canvi.
