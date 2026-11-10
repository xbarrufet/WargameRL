# Fases d’implementació de la simulació

Aquest document defineix l’ordre recomanat per implementar la simulació de
WargameRL a partir de [example.yaml](/Users/xavier/Development/WargameRL/config/example.yaml).
La prioritat és construir primer un motor de joc sense interfície gràfica,
verificable amb proves, i afegir després la visualització.

## Criteri general d’arquitectura

La simulació es divideix en tres parts:

```text
Configuració YAML → Motor de simulació → Visualització Pygame
                                      ↘ Adaptador RL futur
```

El motor és la font única de veritat. La UI només consulta l’estat, mostra les
accions vàlides i envia accions al motor.

## Fase 0 — Preparació del projecte

**Estat: completada.** S’ha creat l’entorn virtual `.venv`, la configuració
del paquet, l’estructura inicial de `src/`, les proves bàsiques, el punt
d’entrada de consola i [INDEX.md](./INDEX.md). La prova smoke
[`test_smoke.py`](../tests/test_smoke.py) s’executa correctament.

### Objectiu

Crear l’estructura Python i fixar les eines bàsiques.

### Tasques

- Crear `pyproject.toml`.
- Crear els paquets `wargame/model`, `wargame/rules`, `wargame/engine`,
  `wargame/io` i `wargame/ui`.
- Configurar `pytest`.
- Afegir dependències: `PyYAML`, `pygame-ce` i `pytest`.
- Afegir un punt d’entrada de consola.

- Mantenir `.venv/` fora del control de versions.

### Resultat

El projecte es pot instal·lar i executar amb una ordre de desenvolupament, i
les proves buides s’executen correctament.

## Fase 1 — Carregador i validador YAML

**Estat: completada.** S’ha implementat `wargame.io.yaml_reader` amb models de
configuració, rutes de sprites relatives al YAML, validació estricta de camps,
coordenades, dimensions, identificadors, orientacions, valors positius i PNG.
També s’han afegit proves de càrrega i errors de configuració.

### Objectiu

Convertir [example.yaml](/Users/xavier/Development/WargameRL/config/example.yaml)
en una configuració interna segura.

### Tasques

- Implementar `yaml_reader.py`.
- Carregar dimensions i matriu d’elevacions.
- Carregar objectius, zones, equips i robots.
- Resoldre les rutes dels sprites relatives al YAML.
- Validar:
  - mapa de 15 files per 17 columnes;
  - elevacions `0` o `1`;
  - coordenades dins del mapa;
  - identificadors únics;
  - robots i objectius no superposats;
  - orientacions vàlides;
  - sprites PNG existents;
  - valors positius de moviment, rang i dany.

### Resultat

Una configuració YAML vàlida crea un objecte de configuració. Una configuració
incorrecta produeix un error indicant el camp afectat.

## Fase 2 — Model de dades

### Objectiu

Definir l’estat de la partida sense implementar encara les regles.

### Components

- `HexCoordinate(q, r)`.
- `Direction` amb `N`, `NE`, `SE`, `S`, `SW`, `NW`.
- `Phase` amb `MOVEMENT`, `SHOOTING`, `SCORING`.
- `Team`.
- `Robot`.
- `Objective`.
- `Board`.
- `GameState`.

### Resultat

Es pot crear un `GameState` complet a partir del YAML i serialitzar-lo per
guardar-lo o inspeccionar-lo.

## Fase 3 — Coordenades i mapa hexagonal

### Objectiu

Implementar les operacions bàsiques del tauler.

### Tasques

- Validar coordenades `q` i `r`.
- Calcular els sis veïns.
- Calcular distància hexagonal.
- Consultar l’elevació d’una casella.
- Detectar caselles ocupades.
- Convertir una coordenada a posició de pantalla.
- Convertir una posició de pantalla a coordenada.

### Resultat

El motor pot consultar el mapa sense dependre de Pygame i la UI futura pot
seleccionar caselles amb el ratolí.

## Fase 4 — Moviment i orientació

### Objectiu

Implementar les accions de moviment, pivot i salt.

### Regles

- El robot pot moure fins a `M` caselles en elevació igual o inferior.
- El salt a una elevació superior només és possible a una casella adjacent.
- El salt consumeix tot el moviment disponible.
- No es pot acabar en una casella ocupada.
- Pivotar 60° consumeix un punt de moviment.
- Els pivots i el moviment es poden combinar.
- El pivot final després del salt és gratuït.

### Tasques

- Crear `MoveAction`, i `PivotAction`.
- Calcular caselles accessibles.
- Validar camins i costos.
- Actualitzar posició i orientació només després de validar tota l’acció.

### Resultat

Es pot moure qualsevol robot de forma segura i el motor retorna les caselles
accessibles i els errors de moviment.

## Fase 5 — Fases i cicle de torn

### Objectiu

Implementar la màquina d’estats de la partida.

### Flux

```text
MOVEMENT → SHOOTING → SCORING → canvi d’equip → MOVEMENT
```

### Regles

- Primer actua l’equip A i després l’equip B.
- No hi ha ordre fix entre els robots del mateix equip.
- Només actua l’equip actiu.
- Cada acció només és vàlida durant la seva fase.
- El final de fase es controla amb `EndPhaseAction`.

### Resultat

Una partida pot avançar de forma completa sense combat, i el motor rebutja
accions que no corresponen a la fase actual.

## Fase 6 — Línia de visió

### Objectiu

Determinar quins robots poden veure’s i disparar-se.

### Tasques

- Calcular l’arc frontal a partir de l’orientació.
- Comprovar la distància màxima `R`.
- Implementar el bloqueig per elevacions.
- Detectar si el blanc té cobertura.
- Retornar el motiu pel qual un blanc no és vàlid.

### Resultat

El motor pot generar la llista de blancs vàlids per a cada robot i la UI pot
ressaltar-los.

### Decisió pendent

Cal fixar l’algoritme exacte per traçar la línia entre dos hexàgons quan el
segment passa entre dues caselles.

## Fase 7 — Combat i dany

### Objectiu

Implementar el dispar i la resolució del dany.

### Regles

- El dispar sempre impacta si compleix rang i línia de visió.
- Es tiren `D` daus de sis cares.
- Armadura frontal: `3+`.
- Armadura lateral: `4+`.
- Armadura posterior: `5+`.
- La cobertura afegeix `+1` a l’armadura.
- Cada dau no aturat genera un impacte.
- Amb 10 impactes el robot queda destruït.

### Tasques

- Crear `ShootAction`.
- Centralitzar el generador aleatori.
- Acceptar una llavor per reproduir partides.
- Retornar un resum del combat: daus, armadura, cobertura i impactes.
- Bloquejar robots destruïts.

### Resultat

Es pot executar un combat reproduïble i inspeccionar-ne el resultat complet.

## Fase 8 — Puntuació i final de partida

### Objectiu

Implementar la puntuació i les condicions de final.

### Regles

- Es puntua al final del torn de l’equip actiu.
- Objectiu de zona pròpia: valor `rules.objective_points.friendly` (1 per defecte).
- Objectiu neutral: valor `rules.objective_points.neutral` (3 per defecte).
- Objectiu de la zona enemiga: valor `rules.objective_points.enemy` (5 per defecte).
- Destruir un robot enemic: 2 punts.
- Un robot continua puntuant mentre es manté dins del radi 4.
- En arribar a 7 punts, l’altre equip pot completar el seu torn.
- Guanya qui té més punts després del torn final.
- Si les puntuacions coincideixen, el resultat és empat.

### Resultat

La simulació pot produir `team_a_wins`, `team_b_wins` o `draw` de forma
determinista, excepte en les tirades de daus controlades per llavor.

## Fase 9 — Simulació per consola

### Objectiu

Provar una partida completa sense gràfics.

### Tasques

- Carregar `config/example.yaml`.
- Mostrar l’estat inicial.
- Permetre introduir accions manualment o executar una seqüència de prova.
- Mostrar cada transició, resultat de combat i puntuació.
- Afegir una opció per fixar la llavor aleatòria.

### Resultat

Es pot verificar el joc complet abans d’implementar la interfície gràfica.

## Fase 10 — Visualització Pygame

### Objectiu

Construir una UI que sigui client del motor.

### Tasques

- Dibuixar la graella hexagonal.
- Pintar elevacions i zones.
- Dibuixar objectius.
- Carregar i reutilitzar els sprites de
  [config/imgs/](/Users/xavier/Development/WargameRL/config/imgs).
- Mostrar els robots amb la seva orientació.
- Seleccionar robot i casella amb el ratolí.
- Ressaltar moviments, salts i blancs vàlids.
- Mostrar fase, torn, puntuacions i missatges d’error.
- Mostrar el resultat final, inclòs l’empat.

### Resultat

La partida es pot jugar manualment amb representació visual, sense duplicar
cap regla dins del renderitzador.

## Fase 11 — Proves i estabilització

### Objectiu

Assegurar que els canvis de la UI no trenquin la simulació.

### Proves mínimes

- Càrrega i errors del YAML.
- Dimensions i límits del mapa.
- Distància i veïns hexagonals.
- Moviment, ocupació, salts i pivots.
- Línia de visió, arcs i cobertura.
- Combat amb llavor fixa.
- Destrucció i puntuació.
- Final amb victòria i empat.
- Seqüència completa de torns.

### Resultat

El motor disposa d’una suite de regressió i qualsevol canvi de regles es pot
validar abans de continuar.

## Fase 12 — Preparació per al RL

Aquesta fase no implementa encara l’agent. Només prepara el límit tècnic per a
una integració posterior.

### Tasques

- Exposar `reset()` per crear un estat inicial.
- Exposar `step(action)` per executar una acció.
- Exposar la llista d’accions vàlides.
- Fer l’estat serialitzable i numèricament representable.
- Separar la recompensa de la puntuació visual.
- Permetre executar el motor sense Pygame.
- Crear posteriorment un adaptador `WargameEnv` compatible amb Gymnasium.

### Resultat

El motor queda preparat per connectar un agent de RL sense modificar les regles
ni la visualització.

## Ordre recomanat de lliuraments

| Lliurament | Fases | Resultat |
|---|---:|---|
| M1 | 0–3 | Configuració carregada i mapa consultable |
| M2 | 4–5 | Moviment i cicle de torn funcionals |
| M3 | 6–8 | Simulació completa amb combat i puntuació |
| M4 | 9 | Partida executable per consola |
| M5 | 10–11 | UI gràfica i proves de regressió |
| M6 | 12 | Frontera preparada per al RL |

La implementació hauria d’aturar-se funcionalment a M5 abans de començar
l’entrenament. Això permet validar que l’entorn de joc és correcte i reproduïble
abans d’utilitzar-lo com a entorn d’aprenentatge.
