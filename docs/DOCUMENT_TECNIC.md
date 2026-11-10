# Document tècnic — WargameRL

## 1. Objectiu i abast

WargameRL és un prototip de simulació i visualització d’un joc tàctic per
torns entre dos equips de robots. La primera fase del projecte no implementa
cap sistema d’intel·ligència artificial ni d’aprenentatge per reforç. El seu
objectiu és disposar d’un motor de joc correcte, observable i fàcil de provar.

El sistema ha de permetre:

- carregar un mapa i una partida des d’un fitxer YAML;
- representar una graella hexagonal de 17 × 15 caselles;
- controlar robots, posicions, orientacions, elevacions i danys;
- executar i validar moviments, pivots, salts i dispars;
- gestionar torns, fases, puntuació i final de partida;
- visualitzar l’estat actual i les accions disponibles;
- executar la simulació sense interfície gràfica per fer proves i, més
  endavant, entrenar agents de Reinforcement Learning.

Queda fora de l’abast inicial la implementació de l’agent de RL, l’entrenament,
la xarxa neuronal i qualsevol sistema de presa de decisions automàtica.

## 2. Tecnologia proposada

Es proposa implementar el projecte en Python amb una arquitectura separada en
tres capes:

```text
Configuració YAML
        ↓
Motor de simulació (sense interfície)
        ↓
Visualització Pygame / adaptador RL futur
```

### 2.1. Components tecnològics

| Component | Tecnologia proposada | Funció |
|---|---|---|
| Llenguatge | Python | Motor, eines, proves i futura integració amb RL |
| Visualització | `pygame-ce` | Finestra, mapa hexagonal, sprites i interacció |
| Configuració | `PyYAML` | Lectura de mapes i partides |
| Model de dades | `dataclasses` i `Enum` | Estat controlat, fases i accions |
| Proves | `pytest` | Proves de regles, simulació i regressions |
| RL futur | Interfície compatible amb Gymnasium | Adaptador futur, separat del motor |

### 2.2. Justificació

Python permet compartir el mateix llenguatge entre el simulador, les proves,
les eines de generació de partides i la futura capa d’aprenentatge per reforç.
`pygame-ce` és suficient per a la visualització 2D del prototip i evita
introduir una dependència de navegador o un motor 3D abans que sigui necessari.

La decisió més important és que el motor no depengui de Pygame. Això permetrà
executar una partida en mode gràfic, en mode text o en mode entrenament amb el
mateix codi de regles.

## 3. Arquitectura del projecte

Una estructura inicial recomanada és:

```text
wargame_rl/
├── config/
│   ├── example.yaml
│   └── imgs/
│       ├── robot_team1.png
│       └── robot_team2.png
├── wargame/
│   ├── model/
│   │   ├── coordinates.py
│   │   ├── entities.py
│   │   ├── enums.py
│   │   └── state.py
│   ├── rules/
│   │   ├── movement.py
│   │   ├── visibility.py
│   │   ├── combat.py
│   │   └── scoring.py
│   ├── engine/
│   │   ├── actions.py
│   │   ├── game.py
│   │   └── validation.py
│   ├── io/
│   │   └── yaml_reader.py
│   └── ui/
│       ├── hex_renderer.py
│       ├── input_controller.py
│       └── pygame_app.py
├── tests/
└── pyproject.toml
```

La separació entre `model`, `rules`, `engine` i `ui` és necessària perquè la
interfície gràfica no pugui modificar directament l’estat de la partida. Tota
acció ha de passar pel motor, que comprova si és vàlida i després produeix el
nou estat.

## 4. Model del mapa

El mapa utilitza coordenades hexagonals axials `q,r`:

- `q`: columna, entre 0 i 16;
- `r`: fila, entre 0 i 14;
- cada casella té una elevació `0` o `1`;
- cada casella pot contenir com a màxim un robot;
- els objectius tenen una posició i una zona (`team_a`, `neutral` o `team_b`).

El mòdul de coordenades ha d’oferir com a mínim:

- validació de coordenades dins del mapa;
- obtenció dels sis veïns d’una casella;
- distància hexagonal entre dues caselles;
- conversió de coordenades de mapa a coordenades de pantalla;
- conversió inversa de pantalla a casella per seleccionar amb el ratolí.

La distància hexagonal s’ha d’utilitzar tant per calcular el rang de les armes
com per comprovar el radi de puntuació dels objectius.

## 5. Entitats principals

### Robot

Cada robot ha de contenir identificador únic, equip, posició `q,r`, orientació,
moviment màxim `M`, rang `R`, dany de l’arma `D`, impactes acumulats i estat
actiu o destruït. Les orientacions possibles són `N`, `NE`, `SE`, `S`, `SW` i
`NW`.

Cada equip té associat un sprite PNG que utilitzen els seus robots. Les imatges
de prova es troben a `config/imgs/robot_team1.png` i
`config/imgs/robot_team2.png`, amb una mida de 84 × 72 píxels. La ruta del
sprite es defineix al nivell de l’equip i és relativa al fitxer YAML carregat.

### Partida

L’estat global ha d’incloure mapa, objectius, robots, equips, equip actiu,
número de ronda, torn, fase, puntuacions, resultat i llavor aleatòria si
s’utilitza aleatorietat.

## 6. Màquina d’estats de la partida

El flux normal és:

```text
INICI DE PARTIDA
       ↓
TORN DE L’EQUIP A
  moviment → dispar → puntuació
       ↓
TORN DE L’EQUIP B
  moviment → dispar → puntuació
       ↓
NOVA RONDA
```

Dins de cada fase no hi ha un ordre fix per als robots. L’usuari pot escollir
qualsevol robot actiu i executar una acció vàlida.

La puntuació es calcula al final del torn de l’equip actiu. Els punts per zona
es configuren amb `rules.objective_points` i són relatius a l’equip que puntua:
`friendly`, `neutral` i `enemy`. Els valors funcionals de l’exemple són 1, 3 i
5, segons [DESCRIPCIO.md](./DESCRIPCIO.md). Un robot que continua dins del radi
d’un objectiu continua puntuant en els torns posteriors.

Quan un equip arriba a 7 punts, l’altre equip pot completar el seu torn si
encara no l’ha jugat. Després es comparen les puntuacions. Guanya l’equip amb
més punts i, si són iguals, el resultat és un empat.

## 7. Accions i validació

Les accions es representaran com a objectes de dades, per exemple:

```text
MoveAction(robot_id, path)
PivotAction(robot_id, orientation)
ShootAction(attacker_id, target_id)
EndPhaseAction()
```

El motor ha de validar abans d’executar una acció que correspon a la fase
actual, que el robot pertany a l’equip actiu, que no està destruït, que el
destí és vàlid i que el moviment o dispar encara estan disponibles. També ha
de comprovar el camí, l’ocupació, el rang i la línia de visió.

Les accions rebutjades no han de modificar l’estat de la partida i han de
retornar un error explicatiu per a la interfície i per a les proves.

## 8. Moviment i orientació

- El robot pot moure fins a `M` caselles en la mateixa elevació o en una
  elevació inferior.
- Arribar a una elevació superior consumeix tot el moviment disponible.
- El salt només és possible cap a una casella adjacent.
- No es pot acabar en una casella ocupada.
- Pivotar 60 graus consumeix un punt de moviment.
- El moviment i els pivots es poden combinar.
- En acabar el moviment, el robot pot fer un pivot gratuït.

El càlcul de moviment ha de retornar les caselles accessibles perquè la UI les
marqui abans que l’usuari confirmi l’acció.

## 9. Línia de visió i combat

El mòdul de visibilitat ha de comprovar l’arc frontal de l’atacant, la distància
màxima de l’arma, el bloqueig produït per les elevacions i la cobertura quan el
blanc és en una elevació superior.

El dispar sempre impacta si compleix rang i línia de visió. El blanc tira `D`
daus de sis cares. La tirada d’armadura depèn de l’angle:

| Zona atacada | Armadura |
|---|---:|
| Frontal | 3+ |
| Lateral | 4+ |
| Posterior | 5+ |

La cobertura afegeix `+1` a la tirada d’armadura. Cada dau que no és aturat
per l’armadura genera un impacte. Quan un robot arriba a 10 impactes, queda
destruït i l’equip contrari rep els punts de destrucció configurats.

La generació aleatòria s’ha de centralitzar en el motor i ha d’acceptar una
llavor. Això permet repetir una partida exactament durant les proves.

## 10. Visualització

La UI de Pygame ha de ser una projecció de l’estat del motor. Com a mínim ha
de mostrar la graella, elevacions, zones, objectius, robots, orientacions,
caselles accessibles, possibles blancs, fase, torn, puntuacions, impactes,
missatges d’error i resultat final.

Els sprites dels equips s’han de carregar una sola vegada i reutilitzar-se per
als robots corresponents. La UI ha de poder girar o orientar visualment el
sprite segons l’orientació del robot, o bé aplicar una fletxa d’orientació
separada si la imatge no és rotacionalment simètrica.

El renderitzador no ha de contenir regles del joc. No ha de decidir si una
casella és accessible; ha de rebre aquesta informació del motor.

## 11. Configuració YAML

El format definit a [DESCRIPCIO.md](/Users/xavier/Development/WargameRL/DESCRIPCIO.md)
ha de ser validat abans de crear l’estat inicial. La descripció funcional és la
font de veritat de les regles; aquest document només descriu l’arquitectura. El
lector ha de comprovar les
dimensions, la matriu d’elevacions, les coordenades, els identificadors, les
orientacions, els valors positius i que hi hagi exactament dos equips.
També ha de validar que cada equip tingui un `sprite`, que la ruta sigui
relativa al fitxer YAML i que el fitxer d’imatge existeixi i sigui un PNG
carregable.

Si la configuració no és vàlida, el programa ha de fallar abans d’iniciar la
partida i mostrar el camp que conté l’error.

## 12. Proves mínimes

Cal implementar proves per a distància i límits hexagonals, moviment, salts,
pivots, línia de visió, cobertura, rang, tirades amb llavor fixa, destrucció,
puntuació repetida, victòria, empat i càrrega del YAML.

## 13. Preparació per al Reinforcement Learning

El RL s’afegirà posteriorment com un adaptador sobre el motor, no com una
responsabilitat de la UI ni de les regles. El motor ha de proporcionar des del
principi:

- estat serialitzable;
- accions codificables i llista d’accions vàlides;
- transicions reproduïbles amb una llavor;
- recompensa separable de la puntuació visual;
- execució sense Pygame;
- una interfície futura equivalent a `reset()` i `step(action)`.

Una futura classe `WargameEnv` podrà adaptar el motor a una interfície de tipus
Gymnasium. La representació exacta de l’observació i de l’espai d’accions es
decidirà quan es defineixi l’agent.

## 14. Decisions pendents

Abans de la implementació completa cal concretar l’algoritme exacte de línia
de visió, el comportament d’un robot destruït durant el torn, les posicions
definitives dels objectius, els valors inicials de `M`, `R` i `D`, i si l’usuari
pot acabar manualment una fase abans d’utilitzar totes les accions disponibles.

## 15. Recomanació d’implementació

La primera fita hauria de ser un motor sense gràfics capaç de carregar el YAML
i executar una partida per consola amb proves automàtiques. Després s’hi hauria
d’afegir la UI de Pygame com a client del motor. Aquesta seqüència permet
validar les regles abans de dedicar temps a l’aspecte visual i deixa preparada
la base per a l’adaptador de RL.
