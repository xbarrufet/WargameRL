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

**Estat: completada.** S’han implementat `HexCoordinate`, les enumeracions de
direcció, fase i resultat, les entitats `Team`, `Robot`, `Objective` i `Board`,
i `GameState`. L’estat inicial es crea a partir de `GameConfig`, valida els
invariants del model i es pot serialitzar i restaurar en format compatible amb
JSON. Els tests del model i del round trip passen correctament.

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

**Estat: completada.** La convenció de la fase és axial `q,r` amb
hexàgons **flat-top**: `N` apunta perpendicularment al costat superior, no a
un vèrtex. La conversió utilitza una mida i un origen configurables i el motor
no depèn de Pygame.

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

**Estat: completada.** S’han implementat les accions de moviment normal,
pivot i salt, amb validació atòmica de pressupost, elevació i ocupació. Els
robots bloquegen el moviment normal però no la trajectòria dels salts; el salt
només exigeix que la casella final estigui lliure. També es poden consultar les
destinacions accessibles i escollir gratuïtament l’encarament final després
d’un salt.

### Objectiu

Implementar les accions de moviment, pivot i salt.

### Regles

- El robot disposa de `M` punts de moviment normal.
- Avançar en la direcció d'encarament costa 1 punt i només permet anar a una
  casella de la mateixa elevació o inferior.
- Pivotar 60° costa 1 punt; els pivots i els avanços es poden combinar.
- Es pot gastar només una part del moviment, inclòs no moure's.
- El salt permet anar fins a `J` hexàgons en qualsevol direcció,
  independentment de l'elevació, i permet passar per sobre de robots.
- El salt no pot acabar en una casella ocupada i permet escollir gratuïtament
  l'encarament final.
- No es pot acabar en una casella ocupada.

### Tasques

- Crear accions per al moviment normal, el pivot i el salt.
- Calcular caselles accessibles.
- Validar camins, costos, elevació, ocupació i límit de salt.
- Actualitzar posició i orientació només després de validar tota l’acció.

### Resultat

Es pot moure qualsevol robot de forma segura i el motor retorna les caselles
accessibles i els errors de moviment.

## Fase 5 — Fases i cicle de torn

**Estat: completada.** El motor implementa les transicions
`MOVEMENT → SHOOTING → SCORING → MOVEMENT` mitjançant `EndPhaseAction`, valida
l’equip actiu i la fase de les accions, aplica la puntuació configurada abans
de canviar d’equip i incrementa la ronda quan tots dos equips han completat el
seu torn. `RulesConfig` es conserva dins de `GameState` per mantenir la
puntuació determinista i serialitzable.

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
- Al final de `SCORING` només puntua l'equip actiu i després es canvia
  d'equip; la ronda avança quan tots dos equips han completat el seu torn.
- El final de fase es controla amb `EndPhaseAction`.

### Resultat

Una partida pot avançar de forma completa sense combat, els robots de l’equip
actiu poden actuar en qualsevol ordre i el motor rebutja accions que no
corresponen a la fase o a l’equip actual.

## Fase 6 — Línia de visió

**Estat: completada.** El motor calcula l’arc frontal de 120° en geometria
flat-top, valida el rang `R`, recorre la línia hexagonal i aplica el bloqueig
per elevacions. Els robots no bloquegen la línia de visió i les consultes
retornen blancs vàlids amb motius deterministes per als rebutjats, sense
introduir cobertura ni regles de combat.

### Objectiu

Determinar quins robots poden veure’s i disparar-se.

### Tasques

- Calcular l’arc frontal a partir de l’orientació.
- Comprovar la distància màxima `R`.
- Implementar el bloqueig per elevacions.
- Retornar el motiu pel qual un blanc no és vàlid.

### Resultat

El motor pot generar la llista de blancs vàlids per a cada robot i la UI pot
ressaltar-los.

La cobertura per elevació no forma part d'aquesta PoC. L’arc frontal de 120°
segueix la projecció flat-top dels costats esquerre i dret de l’encarament,
segons [arc_frontal.png](./arc_frontal.png).

## Fase 7 — Combat i dany

**Estat: completada.** El motor executa dispars reproduïbles durant la fase de
dispar, resol impactes i salvacions, acumula dany, retira robots destruïts i
concedeix els punts de destrucció configurats.

### Objectiu

Implementar el dispar i la resolució del dany.

### Regles

- Cada robot pot disparar com a màxim una vegada per torn.
- El blanc ha d'estar dins de l'arc frontal, ser visible i trobar-se dins de
  `R` hexàgons.
- Per impactar es tira `1D6`; el resultat més el modificador ha d'assolir `H`.
- El modificador és `+1` si el robot no s'ha mogut, `0` si ha fet moviment
  normal i `-2` si ha saltat.
- Després d'un impacte, el defensor tira `D` daus D6 de salvació.
- Armadura frontal: `3+`.
- Armadura lateral: `4+`.
- Armadura posterior: `5+`.
- Cada dau no aturat genera un impacte.
- Amb `robot_max_damage` impactes, per defecte 5, el robot queda destruït i es
  retira del mapa.
- Destruir un robot enemic atorga `robot_destruction_points`, per defecte 3,
  una única vegada.

### Tasques

- Crear `ShootAction`.
- Centralitzar el generador aleatori.
- Acceptar una llavor per reproduir partides.
- Retornar un resum del combat: tirada d'impacte, modificador, salvacions i
  impactes.
- Bloquejar robots destruïts.

### Resultat

Es pot executar un combat reproduïble i inspeccionar-ne el resultat complet.

## Fase 8 — Puntuació i final de partida

**Estat: completada.** El motor calcula el control i la puntuació de cada
objectiu al final de `SCORING`, gestiona la victòria per punts, el límit de 15
rondes i els resultats de victòria o empat.

### Objectiu

Implementar la puntuació i les condicions de final.

### Regles

- Es puntua al final del torn de l’equip actiu.
- Objectiu de zona pròpia: valor `rules.objective_points.friendly` (1 per defecte).
- Objectiu neutral: valor `rules.objective_points.neutral` (3 per defecte).
- Objectiu de la zona enemiga: valor `rules.objective_points.enemy` (5 per defecte).
- Un robot contribueix al control si és a distància `<= objective_radius`, per
  defecte 2.
- Controla l'objectiu l'equip amb més robots dins del radi; en cas d'empat no
  hi ha control ni puntuació.
- Cada objectiu puntua com a màxim una vegada per torn i l'equip pot continuar
  puntuant-lo en torns consecutius mentre el controli.
- Destruir un robot enemic atorga els punts de destrucció durant la resolució
  del combat, no durant la fase de puntuació.
- En arribar a `victory_points` (15 per defecte), s'activa el final de partida.
  Si passa durant el primer torn de la ronda, l'altre equip pot completar el
  seu torn.
- La partida té un límit de 15 rondes; en acabar, guanya qui té més punts i
  en cas d'empat el resultat és `draw`.
- Guanya qui té més punts després del torn final; si les puntuacions
  coincideixen, el resultat és empat.

### Resultat

La simulació pot produir `team_a_wins`, `team_b_wins` o `draw` de forma
determinista, excepte en les tirades de daus controlades per llavor.

## Fase 9 — Simulació per consola

**Estat: completada.** S’ha implementat el CLI `wargame simulate` amb modes
`demo` i `manual`, llavors reproduïbles, sortida de transicions, combats,
puntuacions i resultat final. El mode manual documenta les comandes `help`,
`status`, `end`, `move`, `shoot` i `quit`, i `status` mostra també la posició
i l’estat de cada robot.

### Objectiu

Provar una partida completa sense gràfics.

### Tasques

- Carregar `config/example.yaml`.
- Mostrar l’estat inicial.
- Permetre introduir accions manualment o executar una seqüència de prova.
- Mostrar cada transició, resultat de combat i puntuació.
- Afegir una opció per fixar la llavor aleatòria.
- Mostrar el tancament anticipat per assolir `victory_points` i el límit de
  rondes.

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
- Destrucció i els punts configurables per robot destruït (3 per defecte).
- Control d'objectius amb radi 2, empat i puntuació única per torn.
- Final per 15 punts, final després de completar la ronda i límit de 15
  rondes, inclòs l'empat.
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
