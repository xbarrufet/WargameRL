# Design

## Context

El model ja disposa de `GameState`, `Board`, `Robot`, `Direction` i geometria
axial amb distància i veïns. La configuració ja carrega `movement` i `jump` per
robot. La nova lògica ha de romandre al motor, sense dependències de Pygame ni
de les capes Micro AI o Macro AI.

## Goals / Non-Goals

**Goals:**

- Separar la validació de moviment normal i salt de la mutació de l'estat.
- Reutilitzar la geometria i l'ocupació existents com a font única de veritat.
- Fer que una acció invàlida no deixi efectes parcials.
- Conservar informació suficient sobre el tipus de moviment per a la futura
  resolució del dispar.

**Non-Goals:**

- No implementar encara la màquina de fases ni `EndPhaseAction`.
- No implementar línia de visió, combat, puntuació o IA.
- No afegir regles de moviment que no apareguin a `docs/GAME_RULES.md`.

## Decisions

- **Accions explícites per tipus:** es diferenciarà el moviment normal del salt
  perquè tenen costos, trajectòries i restriccions diferents. Una alternativa
  era una acció genèrica amb flags, però faria més fàcil barrejar regles.
- **Seqüència normal validada com un tot:** es calcularà una còpia o pla
  provisional de posició/orientació/cost i només es confirmarà al final. Això
  evita rollback parcial quan una passa falla.
- **Salt per distància axial:** el destí es valida amb la distància hexagonal;
  no es valida la trajectòria perquè les regles permeten travessar robots i
  elevacions durant el salt.
- **Ocupació derivada de `GameState`:** els robots no destruïts bloquegen cada
  pas i destí del moviment normal, però no bloquegen la trajectòria d'un salt;
  sí que bloquegen el destí final del salt. Els robots destruïts no bloquegen
  cap moviment. Els objectius no són obstacles de moviment segons el contracte
  actual.
- **Orientació controlada pel model:** qualsevol orientació final ha de ser
  membre de `Direction`; el salt no consumeix punts per establir-la.

## Risks / Trade-offs

- [Risk] La futura API de torn pot necessitar registrar si el robot ha corregut
  o saltat → Mitigació: retornar un resultat de moviment amb el tipus d'acció i
  reservar camps d'estat explícits sense duplicar la posició.
- [Risk] Una API massa lligada a classes concretes dificultaria l'adaptador RL
  → Mitigació: mantenir accions i resultats amb dades simples i errors de
  validació deterministes.
- [Risk] Una ruta normal pot canviar d'orientació i fer que el següent avanç no
  sigui vàlid → Mitigació: validar cada pas en ordre sobre l'estat provisional.

## Migration Plan

1. Afegir les accions, resultats i validadors al motor.
2. Afegir proves unitàries sobre l'exemple de configuració i casos límit.
3. Integrar l'execució amb `GameState` sense canviar la serialització existent.
4. Executar la suite completa i la validació OpenSpec.
