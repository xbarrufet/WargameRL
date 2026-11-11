# Design

## Context

El model ja disposa de coordenades axials, distància hexagonal, elevacions,
orientacions i estat de robots. No existeix encara un mòdul de visibilitat i la
implementació ha de romandre al motor de joc, sense Pygame ni dependències de
les capes d’IA.

## Goals / Non-Goals

**Goals:**

- Separar la classificació geomètrica de l’arc de la validació de rang i
  elevació.
- Retornar resultats explicables i deterministes per a la UI i el combat futur.
- Tractar els robots com a entitats que no bloquegen la línia de visió.
- Reutilitzar `HexCoordinate`, `Board` i `Direction` com a font única de
  geometria.

**Non-Goals:**

- No implementar `ShootAction`, tirades, salvacions ni dany.
- No aplicar bonificacions de cobertura per elevació.
- No implementar decisions de la UI ni cap política d’IA.

## Decisions

- **API de consulta pura:** la visibilitat serà una consulta sense mutar
  `GameState`, amb un resultat que separi blancs vàlids i motius de rebuig.
- **Arc frontal de 120° derivat de sectors hexagonals:** la classificació usarà
  la convenció de les sis orientacions i la geometria axial existent. En
  flat-top, els límits són la projecció dels costats esquerre i dret de
  l’encarament, segons `docs/arc_frontal.png`, en lloc de coordenades de
  pantalla o angles de Pygame.
- **Línia canònica del tauler:** la comprovació d’elevació recorrerà les
  caselles interposades de la línia hexagonal entre origen i destí. Els robots
  es poden ignorar perquè només el terreny participa en el bloqueig.
- **Elevació de l’origen com a alçada de visió:** una posició alta pot veure per
  sobre del terreny elevat; el bloqueig només s’aplica al cas específic de dos
  extrems baixos amb terreny alt interposat.
- **Motius tipats:** els motius de rebuig seran valors estables del motor,
  perquè la UI i les proves no depenguin de textos d’error canviants.

## Risks / Trade-offs

- [Risk] Els límits de 120° poden ser sensibles a la convenció axial →
  Mitigació: cobrir les sis orientacions, els dos límits de l’arc i les
  caselles dels eixos amb proves basades en `docs/arc_frontal.png`.
- [Risk] Una línia hexagonal pot tenir decisions d’arrodoniment en casos
  simètrics → Mitigació: centralitzar la línia canònica en la geometria del
  motor i provar els casos intermedis.

## Migration Plan

1. Afegir els tipus de resultat i motiu de visibilitat.
2. Implementar arcs, rang i bloqueig per elevacions.
3. Afegir proves de regressió i exports del motor.
4. Actualitzar la documentació de la fase 6 i executar la suite completa.
