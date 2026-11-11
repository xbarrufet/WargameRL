# Design

## Context

La fase 2 ja disposa de `HexCoordinate`, `Board` i `GameState`, però les
coordenades només són dades. La fase 3 ha de fer operativa la geometria sense
introduir dependències de Pygame ni anticipar les regles de moviment o de línia
de visió.

## Goals / Non-Goals

**Goals:**

- Centralitzar la convenció axial `q,r` i els sis vectors veïns.
- Fer que distància, límits, elevació i ocupació siguin reutilitzables pel motor.
- Fixar una projecció i una inversa per a hexàgons flat-top.
- Fer les operacions deterministes i fàcilment testables.

**Non-Goals:**

- Implementar moviment, pivots, salts, arcs frontals o línia de visió.
- Dibuixar hexàgons o carregar Pygame al model.
- Decidir costos de moviment o comportament de la UI.

## Decisions

- **Coordenades axials:** es manté `q,r` com a contracte públic. La distància
  usa `s = -q-r` i `max(abs(dq), abs(dr), abs(ds))`.
- **Veïns:** s’utilitzen els vectors `(+1,0)`, `(+1,-1)`, `(0,-1)`,
  `(-1,0)`, `(-1,+1)` i `(0,+1)`. L’ordre serà estable però no imposarà el
  significat de les orientacions de robots.
- **Flat-top:** amb radi `size`, origen `(ox, oy)` i coordenada axial, el
  centre és `x = ox + size * 3/2 * q` i
  `y = oy + size * sqrt(3) * (r + q/2)`. Això manté l’orientació `N`
  perpendicular al costat superior, tal com fixa `GAME_RULES.md`.
- **Inversa pantalla:** es converteix primer a coordenades axials fraccionàries,
  s’aplica arrodoniment cúbic i després es comprova si el punt és realment dins
  del polígon flat-top i dels límits del tauler. Això evita seleccionar el
  hexàgon adjacent en les fronteres.
- **Ocupació:** la consulta es deriva de les posicions actuals dels robots i
  no manté una segona font de veritat. Els objectius no es consideren robots
  ocupants per a les futures regles de moviment.
- **API sense Pygame:** la projecció treballa amb tuples o tipus numèrics
  simples; la capa UI serà responsable de transformar-los en primitives de
  Pygame.

## Risks / Trade-offs

- [Risk] Les vores entre hexàgons poden produir empats numèrics → Mitigació:
  utilitzar tolerància explícita i una regla estable de desempatat en la
  conversió inversa.
- [Risk] La convenció axial pot no coincidir amb una UI futura → Mitigació:
  deixar origen i mida configurables i mantenir la transformació documentada
  en un únic mòdul.
- [Risk] La forma actual de `Board` encara és una tupla d’elevacions →
  Mitigació: afegir només consultes derivades, sense canviar la serialització
  pública de l’estat.

## Migration Plan

1. Afegir les utilitats geomètriques i els tests sense canviar el YAML.
2. Connectar `Board` i `GameState` a les consultes de límits, elevació i
   ocupació.
3. Actualitzar la documentació de la convenció flat-top.
4. Verificar amb tota la suite de tests abans que les fases de moviment o UI
   consumeixin aquestes operacions.
