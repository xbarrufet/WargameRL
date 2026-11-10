# Design

## Context

La configuració actual conté `objective_radius`, `victory_points` i
`robot_destruction_points`, però els punts per zona només apareixen com a
constants documentades. `DESCRIPCIO.md` és la font funcional i estableix 1, 3 i
5; `DOCUMENT_TECNIC.md` conté una versió inconsistent que cal corregir.

## Goals / Non-Goals

**Goals:**

- Fer configurables els punts per relació de zona.
- Mantenir una semàntica comuna per als dos equips.
- Validar els valors en el carregador YAML abans de crear l’estat.
- Preparar l’objecte de regles perquè la fase de puntuació el pugui consumir.
- Eliminar la contradicció documental.

**Non-Goals:**

- Implementar encara la fase completa de puntuació.
- Canviar el radi d’objectius, la victòria o els punts per destrucció.
- Definir punts diferents per `team_a` i `team_b` quan la relació és la mateixa.

## Decisions

- **Claus `friendly`, `neutral`, `enemy`:** expressen la relació amb l’equip
  que puntua i eviten duplicar regles per a A i B.
- **Valors obligatoris i no negatius:** segueixen la validació estricta de la
  fase 1 i fan que una configuració no documentada falli aviat.
- **Valors per defecte funcionals 1/3/5:** provenen de `DESCRIPCIO.md`, que el
  projecte ja declara com a font de regles.
- **Camp dins de `rules`:** manté els paràmetres de puntuació agrupats amb la
  resta de regles i permet que `RulesConfig` els exposi al motor.
- **Documentació tècnica referencial:** `DOCUMENT_TECNIC.md` explicarà el
  model i enllaçarà amb la descripció funcional, sense repetir constants.

## Risks / Trade-offs

- [Risk] Les configuracions antigues no tindran el nou bloc → es considera un
  canvi incompatible explícit i s’actualitza la configuració d’exemple.
- [Risk] La futura puntuació pot interpretar malament `team_a`/`team_b` → la
  spec fixa que els valors són relatius a l’equip que puntua.

## Migration Plan

Afegir `rules.objective_points` a cada YAML existent amb `friendly: 1`,
`neutral: 3` i `enemy: 5`. Actualitzar els tests i la documentació abans de
començar la implementació de la fase de puntuació.
