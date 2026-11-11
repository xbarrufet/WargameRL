# GAME_RULES — WargameRL

## 1. Propòsit i autoritat

Aquest document és la font de veritat de les **regles del joc** de WargameRL. `DESCRIPCIO.md` descriu la PoC, els components i l'arquitectura, però no redefineix aquestes regles. Els fitxers YAML configuren escenaris concrets i han de respectar aquest contracte.

## 2. Equips i seqüència de joc

- Dos equips, inicialment amb **2 robots per equip**.
- El joc es desenvolupa per torns d'equip: primer actua un equip i després l'altre.
- Cada torn consta de tres fases, en aquest ordre: **moviment, dispar i puntuació**.
- Dins de cada fase, els robots de l'equip actiu poden actuar en qualsevol ordre.
- Cada robot té una arma principal i una orientació sobre el mapa hexagonal.

## 3. Mapa i objectius

- Mapa hexagonal de **17 × 15** caselles, identificades per coordenades `q,r`.
- La representació visual utilitza hexàgons **flat-top**, amb costats superior i inferior horitzontals.
- Tres zones: inicial de l'equip A, neutral i inicial de l'equip B. Les zones inicials ocupen una franja de 5 hexàgons als extrems superior i inferior del mapa.
- **2 objectius per zona**, 6 en total.
- Cada hexàgon té elevació **0 (baixa)** o **1 (alta)**.
- Radi de control dels objectius: **2 hexàgons** (inclosa la casella de l'objectiu).
- Distància hexagonal mínima entre qualsevol parella d'objectius: **5 hexàgons**, de manera que els seus radis de control no se solapin.

## 4. Robots

Paràmetres inicials comuns a tots els robots:

| Paràmetre | Valor |
|---|---:|
| Moviment normal (`M`) | 3 punts |
| Salt (`J`) | 4 hexàgons |
| Rang de l'arma (`R`) | 5 hexàgons |
| Dany de l'arma (`D`) | 2 daus D6 |
| Tirada base per impactar (`H`) | 4+ en 1D6 |
| Resistència | 5 impactes |
| Salvació frontal | 3+ |
| Salvació lateral | 4+ |
| Salvació posterior | 5+ |

**Nota:** `R` és el rang de l'arma; el radi dels objectius és `objective_radius`.

## 5. Moviment

### Moviment normal

- Cada robot disposa de `M=3` punts de moviment.
- Avançar una casella en la direcció d'encarament costa 1 punt.
- Pivotar 60° costa 1 punt; es poden combinar pivots i avanços lliurement dins del pressupost.
- Només es pot avançar a una casella de la mateixa elevació o inferior.
- No es pot travessar una casella ocupada per un altre robot.
- Es permet no gastar tots els punts de moviment, inclòs quedar-se quiet.

### Salt

- Permet desplaçar-se fins a `J=4` hexàgons en qualsevol direcció, independentment de l'elevació.
- Permet passar per sobre d'altres robots.
- En acabar, el robot escull lliurement l'encarament final.
- No es pot acabar en una casella ocupada.

## 6. Línia de visió i orientació

- L’orientació d’un robot apunta perpendicularment a un costat del seu hexàgon; no apunta a un vèrtex.
- Amb orientació `N`, el robot mira cap al costat superior i l’arc frontal és el sector de caselles que s’obre cap amunt, tal com mostra la il·lustració de la PoC.
- Les orientacions `NE`, `SE`, `S`, `SW` i `NW` giren aquest patró en salts de 60°.
- Un robot només pot disparar contra objectius dins del seu **arc frontal**.
- L’arc posterior és el sector oposat a l’arc frontal. Les caselles que no pertanyen a cap d’aquests dos sectors són laterals.
- Les elevacions altes bloquegen la visió entre posicions baixes si queden interposades.
- Un robot situat en elevació alta pot veure per sobre del terreny elevat, i també és visible des de posicions baixes si es troba dins del seu arc de visió.
- **No s'aplica cap bonificació de cobertura per elevació** en aquesta PoC.
- Els robots **no bloquegen** la línia de visió.

## 7. Dispar i dany

- Cada robot pot efectuar **com a màxim un dispar per torn** durant la fase de dispar.
- Per disparar cal que el blanc estigui dins de l'arc frontal, sigui visible i estigui a distància màxima `R=5`.
- Per impactar es tira **1D6**; el resultat modificat ha d'igualar o superar `H=4`.

| Moviment del robot durant el torn | Modificador a impactar |
|---|---:|
| No s'ha mogut | +1 |
| Moviment normal | 0 |
| Ha saltat | −2 |

- Si el dispar impacta, el defensor tira `D=2` daus D6 de salvació.
- Cada dau que iguala o supera el valor d'armadura de l'arc atacat anul·la un impacte; cada salvació fallada causa **1 impacte de dany**.
- L'armadura és 3+ frontal, 4+ lateral i 5+ posterior.
- Quan un robot acumula **5 impactes de dany**, és destruït i es retira del mapa.
- Destruir un robot enemic atorga **3 punts**, una única vegada, a l'equip que l'ha destruït.

## 8. Control i puntuació

- Al final del torn d'un equip, **només puntua l'equip actiu**.
- Un robot contribueix al control d'un objectiu quan està a distància hexagonal **≤ 2**.
- Un objectiu el controla l'equip amb més robots dins del radi. En cas d'empat, no el controla ningú i no puntua.
- Cada objectiu només pot puntuar **una vegada per torn**.
- Un equip pot continuar puntuant un objectiu en torns consecutius mentre el controli.

| Ubicació de l'objectiu respecte de l'equip actiu | Punts per torn |
|---|---:|
| Zona inicial pròpia | 1 |
| Zona neutral | 3 |
| Zona inicial enemiga | 5 |

## 9. Final de partida

- Quan un equip arriba a **15 punts**, s'activa el final de partida.
- Si és el primer equip de la ronda, el segon té dret a completar el seu torn.
- En acabar, guanya l'equip amb més punts. En cas d'igualtat, la partida acaba en empat.

## 10. Configuració i validacions

El YAML defineix les dimensions i elevacions del mapa, els objectius, els equips, els robots i els paràmetres configurables. Com a mínim, el lector ha de validar:

- Dimensions i forma de la matriu d'elevacions (`elevations[r][q]`), i valors 0 o 1.
- Coordenades dins dels límits del mapa i absència d'identificadors duplicats.
- Posicions inicials de robots no superposades.
- Els robots poden compartir casella amb objectius; els objectius no ocupen físicament la casella.
- Orientacions vàlides: `N, NE, SE, S, SW, NW`.
- Valors numèrics positius per a moviment, salt, rang, dany i resistència.
- Separació mínima de 5 hexàgons entre objectius.

Exemple de valors configurables (fragment, no escenari complet):

```yaml
rules:
  objective_radius: 2
  minimum_objective_distance: 5
  victory_points: 15
  robot_destruction_points: 3
  objective_points: {friendly: 1, neutral: 3, enemy: 5}
  armor: {front: 3, side: 4, rear: 5}
  robot_max_damage: 5
  orientations: [N, NE, SE, S, SW, NW]

# Camps de cada robot:
# movement: 3
# jump: 4
# hit_target: 4
# range: 5
# damage: 2
```

## 11. Decisions de final de partida

- Si el primer equip que arriba a 15 punts és també el segon equip de la ronda
  que arriba a aquesta puntuació, el resultat és **empat**.
- La partida té un límit de **15 rondes** per evitar partides indefinides.
