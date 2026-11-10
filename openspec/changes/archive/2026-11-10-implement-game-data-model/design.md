# Design

## Context

La fase 1 produeix `GameConfig` i els seus objectes de configuració, però el
paquet `model` encara és buit. La fase 2 necessita convertir aquesta entrada en
un estat de partida que les fases de coordenades, accions, combat i UI puguin
consumir sense dependre del YAML ni de Pygame.

## Goals / Non-Goals

**Goals:**

- Separar configuració immutable de l’estat mutable de la partida.
- Definir les entitats i enumeracions bàsiques del domini.
- Crear un estat inicial complet a partir de `GameConfig`.
- Oferir una representació JSON-compatible i un round trip verificable.
- Validar invariants de construcció sense implementar regles d’acció.

**Non-Goals:**

- Calcular veïns, distàncies o conversions pantalla/hexàgon de la fase 3.
- Executar moviment, pivots, salts, dispars o puntuació.
- Gestionar transicions de fases o torns.
- Carregar sprites amb Pygame o implementar la UI.

## Decisions

- **Dataclasses i enums del domini:** permeten un model explícit i fàcil de
  provar; s’evita usar diccionaris lliures com a estat principal.
- **`GameConfig` com a entrada:** reutilitza la validació de fase 1 i evita
  duplicar la validació del YAML dins del model.
- **Estat mutable controlat:** la configuració es manté immutable, mentre que
  danys, puntuacions, fase i torn són propietat de `GameState` perquè les fases
  posteriors els puguin actualitzar.
- **Serialització amb primitives:** la sortida serà una estructura de
  diccionaris i llistes compatible amb JSON; les rutes de sprites es
  serialitzaran com a text i les enumeracions com els seus noms.
- **Valors inicials deterministes:** l’equip A, ronda 1, torn 1, fase de
  moviment, puntuacions zero i resultat pendent formen l’estat inicial.

## Risks / Trade-offs

- [Risk] El model pot evolucionar i trencar serialitzacions antigues → incloure
  una versió de model quan s’estabilitzi el format de persistència.
- [Risk] La còpia d’entitats pot permetre divergència respecte de `GameConfig`
  → construir l’estat una sola vegada i afegir proves d’equivalència.
- [Risk] La geometria hexagonal encara no està resolta → mantenir `HexCoordinate`
  com a valor de dades i deixar les operacions geomètriques per a la fase 3.

## Migration Plan

No hi ha migració de dades existent. La implementació haurà d’afegir els mòduls
del paquet `model`, tests i la integració de construcció des de `GameConfig`.
