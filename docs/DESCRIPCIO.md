# WARGAME REINFORCE LEARNING
Es una prova de concepte per l'entrenament de un sistema de RL per jugar a wargames
L idea es poder fer servir RL per la estratgia macro del joc i scripting per la tactica micro del joc

## Regles del Joc
Com a domini del joc, es represtanra la lluita entre 2 equips de robots (inicialement de 2 robots). La mecanica inicial es molt simple.
- Moviment: els robots mouen <M> caselles
- Arma: els robots tenen 1 arma principal de rang <R>  Dany <D>
- Armadura: els robots tene una armadura de 3+ Davant, +4 costats, +5 darrera
El combat es per torns, primer tot l'equip i despres l'altre i hi ha 3 fases per torn
- fase Movimient
- fase dispar
- fase puntuacio

### Puntuacio
Al final del torn de cada equip només es calculen els punts del jugador que ha
acabat el torn.
- Esta a un radi de 4 de un objectiu a la zona inicial : 1 punt
- Esta a un radi de 4 de un objectiu a la zona de ningu : 3 punt
- Esta a un radi de 4 de un objectiu a la zona inicial del enemic : 5 punt
- destrueix 1 robot enemic : 2 punts
Si el robot es queda al meteix objectiu continua puntuant
Un objectiu nomes puntua 1 cop per torn, es a dir si hi ha dos models del mateix equip dins del radi del mateix objectiu nomes es puntua 1 vegada
A un objectiu poden haver models de diferents equips en radi, en aquest cas puntua el equip que tingui mes models en radi, si tenen el mateix, no puntua


### Terreny
El terreny es una grid de hexagons de 17 x 15 hexagons. la zona inicial es troba a la part alta i baixa en un ample de 5 hexagons
Hi ha 2 objectus a cada zona, inicial A, inicial B,i Zona de ningu 
El terreny te 2 elevacions, 

### Linea de visio
un robot veu el tot l'arc frontal seu sempre, pero una elevacio superior tapa les elevacions inferiors de darrera.
Un robot a elevacion alta veu totes les elevacions, pero es vist per tothom

### Moviemnt
Un robot mou tantes caselles como moviment <M> tingui en la mateixa elevacio o inferior, per moure a una elevacio superior gasta tot el moviment (salta). El salt només es pot fer a una casella adjacent.
Pivotar 60º costa 1 punt de moviemnt
Un robot no pot acabar a una casella ocupada per un altre robot
El moviment i el pivot es poden combinar lliurement. En acabar el moviment, el robot pot pivotar gratuïtament.

### Disparo
per disparar el robot ha de tenir linea de visio anb el target i el target ha d'estar a una distancia maxim rang <R>.
Sempre impacta, llavors el target tiran tants daus de 6 cares com dany <D> te l'arma, i depenen d'on ve l'atac (davant, costat, darrera) cada dau que supero la tirada (3+,4+ o 5+), el para la armadura, els altres generen impactes, al arribar a 10 impactes el robot es destruit
Si el robot target es troba a una elevacio superior del que dispara, te covertura, la cobertura dona un +1 a la tirada de armadura

### Final del joc
Qui arribi a 7 punts activa el final de la partida. Si és el primer jugador,
el segon té dret a completar el seu torn. Després es comparen les puntuacions:
guanya el jugador amb més punts i, si les puntuacions són iguals, la partida
acaba en empat.


## Compoenents de la aplicacio
### Mapa UI
Component que dibuixa un grid de hexagons en coordenades q,r de A x B hexagons
Es capaça de pintar hexagons de diferents colors i de posa un dibuix en un encarament determinat a un hexagon
Permet fer accions sobre els elements seleccio robot + seleccion casell target (pot ser moviment, salto, disparo)
### Game
Control del joc, controla les fases, mapa i posicio dels robots i excuta accions mirant que siguin valides. Dins d'una fase, els robots poden actuar en qualsevol ordre; no hi ha un ordre d'actuacio fix.

### Map reader
La configuracio del mapa i de la partida es defineix en un fitxer YAML. Les
coordenades utilitzen el sistema hexagonal `q,r`, amb `q` entre 0 i 16 i `r`
entre 0 i 14.

Exemple d'estructura:

```yaml
schema_version: 1

map:
  width: 17
  height: 15
  # Matriu de 15 files per 17 columnes. Cada valor representa l'elevacio:
  # 0 = baixa i 1 = alta.
  elevations:
    - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    - [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    - [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    - [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

objectives:
  - id: objective_a_1
    position: {q: 2, r: 2}
    zone: team_a
  - id: objective_a_2
    position: {q: 6, r: 2}
    zone: team_a
  - id: objective_neutral_1
    position: {q: 7, r: 7}
    zone: neutral
  - id: objective_neutral_2
    position: {q: 9, r: 7}
    zone: neutral
  - id: objective_b_1
    position: {q: 10, r: 12}
    zone: team_b
  - id: objective_b_2
    position: {q: 14, r: 12}
    zone: team_b

teams:
  - id: team_a
    robots:
      - id: team_a_robot_1
        movement: 3       # M
        range: 5          # R
        damage: 2         # D: nombre de daus de sis cares
        position: {q: 2, r: 0}
        orientation: N
      - id: team_a_robot_2
        movement: 3
        range: 5
        damage: 2
        position: {q: 6, r: 0}
        orientation: NE

  - id: team_b
    robots:
      - id: team_b_robot_1
        movement: 3
        range: 5
        damage: 2
        position: {q: 10, r: 14}
        orientation: S
      - id: team_b_robot_2
        movement: 3
        range: 5
        damage: 2
        position: {q: 14, r: 14}
        orientation: SW

rules:
  objective_radius: 4
  victory_points: 7
  robot_destruction_points: 2
  objective_points: {friendly: 1, neutral: 3, enemy: 5}
  armor: {front: 3, side: 4, rear: 5}
  robot_max_damage: 10
  orientations: [N, NE, SE, S, SW, NW]
```

El lector ha de validar que la matriu tingui exactament 15 files i 17 valors
per fila, que cada elevacio sigui `0` o `1`, que les coordenades siguin dins
del mapa, que no hi hagi robots ni objectius duplicats i que les orientacions
pertanyin al conjunt definit. Els valors de `movement`, `range` i `damage`
han de ser enters positius.


