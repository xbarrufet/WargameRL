# Design

## Context

El model `GameState` ja conserva la fase, l’equip actiu, la ronda, el torn i
les puntuacions. El motor també exposa moviment i les regles de puntuació
existeixen separadament. Per poder puntuar de manera determinista, l’estat
conservarà una instància immutable de `RulesConfig` procedent del YAML. La nova
capacitat ha d’orquestrar aquests components sense introduir dependències de
Pygame, Micro AI o Macro AI.

## Goals / Non-Goals

**Goals:**

- Centralitzar les transicions vàlides del cicle de torn.
- Validar la fase i l’equip actiu abans de delegar qualsevol acció.
- Fer atòmica la finalització de fase, inclosa la puntuació i el canvi d’equip.
- Mantenir l’ordre dels robots lliure dins de cada fase.

**Non-Goals:**

- No implementar encara línia de visió, combat o resolució del dany.
- No canviar les regles de puntuació ni la seva configuració.
- No afegir ordre fix d’activació dels robots.
- No introduir lògica d’IA ni interfície gràfica.

## Decisions

- **Màquina de transicions explícita:** `EndPhaseAction` serà l’única entrada
  que avança de fase. Això evita salts implícits i fa determinista el cicle.
- **Validació a la frontera del motor:** la validació de l’equip actiu i de la
  fase es farà abans de delegar moviment, dispar o puntuació. Una alternativa
  seria repartir-la entre cada regla, però augmentaria el risc d’inconsistències.
- **Puntuació abans del canvi d’equip:** la transició des de `SCORING` calcula
  la puntuació de l’equip actual i només després canvia l’equip actiu. En tornar
  al primer equip, incrementa la ronda.
- **Estat provisional per a transicions:** la puntuació i el canvi de fase es
  validaran sobre un pla provisional i es confirmaran al final per evitar
  estats parcials si la puntuació falla.
- **Identitat d’equips segons l’estat:** l’ordre dels dos equips es deriva de
  l’estat inicial/configuració; no es codifica una dependència amb noms concrets
  com `team_a` o `team_b`.
- **Regles dins de l’estat:** `RulesConfig` es conserva com a dada immutable de
  `GameState`, es valida en construir/restaurar l’estat i participa en el
  round-trip JSON. Això evita que `SCORING` depengui d’un context global o
  mutable.

## Risks / Trade-offs

- [Risk] Les fases futures poden necessitar registrar accions ja executades →
  Mitigació: mantenir els camps de moviment i dispar separats del mecanisme de
  transició i ampliar l’estat només amb requisits aprovats.
- [Risk] Una puntuació amb efectes parcials podria deixar un torn inconsistent
  → Mitigació: validar i aplicar la transició completa de `SCORING` de forma
  atòmica.

## Migration Plan

1. Afegir les accions i validadors de transició al motor.
2. Integrar-los amb `GameState` i les regles de puntuació existents.
3. Afegir proves de fases, equips actius i final de ronda.
4. Executar la suite completa i la validació OpenSpec.
