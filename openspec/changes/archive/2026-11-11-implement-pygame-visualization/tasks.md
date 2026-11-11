# Tasks

## 1. UI foundation

- [x] 1.1 Defineix el controlador de partida gràfic i el punt d’entrada Pygame, carregant YAML i creant l’estat mitjançant les API existents; verifica que el CLI actual continua iniciant-se i que el mode gràfic pot crear una finestra o superfície headless.
- [x] 1.2 Implementa la conversió de coordenades i el renderer de la graella flat-top, elevacions, zones i objectius; verifica amb una prova que les coordenades límit i una casella coneguda es projecten de manera coherent.
- [x] 1.3 Implementa la càrrega, escala i orientació visual dels sprites configurats i el dibuix dels robots; verifica que `config/example.yaml` renderitza tots els equips i robots sense fallar per rutes relatives.

## 2. Interaction and engine integration

- [x] 2.1 Afegeix selecció de robots i caselles amb el ratolí, ressaltat de selecció i conversió píxel-coordenada; verifica amb proves d’entrada que els clics fora del tauler no creen coordenades vàlides.
- [x] 2.2 Connecta les consultes d’accessibilitat de moviment, salts i blancs vàlids al renderer; verifica que les caselles ressaltades coincideixen amb les respostes del motor i no amb una regla duplicada.
- [x] 2.3 Connecta les accions de moviment, salt, dispar i final de fase al controlador del motor; verifica accions vàlides i rebutjades, inclòs que un error conserva l’estat i es mostra a la UI.
- [x] 2.4 Implementa el panell d’informació de fase, equip actiu, ronda, puntuacions, dany i missatges; verifica que es refresca després d’una transició, combat o puntuació.

## 3. Terminal states and verification

- [x] 3.1 Implementa la pantalla o overlay de final amb causa, puntuacions i resultat `team_a_wins`, `team_b_wins` o `draw`; verifica els tres resultats amb estats de prova controlats.
- [x] 3.2 Afegeix proves d’integració headless del client Pygame i documenta l’ordre d’execució gràfica i els controls; verifica que la suite completa del projecte continua passant.
- [x] 3.3 Executa una partida manual amb `config/example.yaml` i comprova visualment mapa, seleccions, opcions, errors, puntuació i final; registra qualsevol ajust de layout necessari abans d’arxivar el canvi.
