# Proposal

## Why

La fase 4 és el primer punt on el motor ha d'aplicar les regles de moviment
definides a `docs/GAME_RULES.md`. Actualment el model ja conserva posició,
orientació, elevació i els paràmetres `movement`/`jump`, però encara no existeix
una API que validi i executi moviment normal, pivots i salts de manera segura.

## What Changes

- Afegir una capacitat de moviment del motor amb accions explícites i
  validables.
- Implementar el moviment normal cap endavant amb cost per casella i per pivot,
  límit `M`, elevació vàlida i bloqueig per robots en cada pas.
- Implementar el salt fins a `J` hexàgons en qualsevol direcció i elevació,
  permetent travessar robots però no acabar en una casella ocupada.
- Permetre escollir lliurement l'orientació final d'un salt.
- Exposar caselles accessibles i errors de validació sense introduir
  dependències de Pygame.
- Afegir proves unitàries per a costos, elevacions, ocupació, límits i
  actualitzacions atòmiques de l'estat.

## Capabilities

### New Capabilities

- `movement-actions`: validació i execució determinista del moviment normal,
  pivots i salts dins del motor de joc.

### Modified Capabilities

Cap.

## Impact

- Nous tipus d'acció i lògica de regles sota `src/wargame/`.
- Integració amb `GameState`, `Board`, `Robot`, `HexCoordinate` i `Direction`.
- Nous tests de moviment i possibles ajustos d'exports del paquet.
- Cap dependència nova i cap canvi a la UI o al comportament de combat.
