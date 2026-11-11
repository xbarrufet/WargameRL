# Design

## Context

El projecte ja disposa d’un motor sense dependència de Pygame, d’un model serialitzable, geometria hexagonal i un CLI funcional. La UI nova ha de respectar aquesta frontera: el motor conserva l’estat i resol les accions; la UI només tradueix esdeveniments d’entrada a accions i dibuixa resultats.

## Goals / Non-Goals

**Goals:**

- Crear un client Pygame interactiu per a una partida carregada des de YAML.
- Centralitzar el cicle d’actualització i renderització en un controlador de UI petit.
- Reutilitzar les conversions de coordenades i les consultes del motor.
- Fer visibles les seleccions, opcions vàlides, errors i estats terminals.

**Non-Goals:**

- No canviar cap regla de `GAME_RULES.md`.
- No afegir una segona representació de `GameState` ni una resolució local d’accions.
- No implementar encara una UI d’entrenament RL, xarxa, editor de mapes o multijugador.

## Decisions

### Client lleuger sobre les API existents

La UI mantindrà una referència a l’estat/controlador del motor i consultarà accions accessibles i blancs vàlids. Les confirmacions crearan accions públiques i les enviaran al motor. Això evita duplicació i permet que consola i Pygame comparteixin comportament.

Alternativa descartada: calcular moviments o arcs dins de la UI; faria possible que la representació contradigués la font de veritat.

### Separació entre renderització, entrada i presentació

El paquet `ui` es dividirà conceptualment en conversió/renderització, estat de selecció i bucle d’entrada. El renderitzador rebrà dades del motor i no gestionarà transicions de fases ni puntuació.

Alternativa descartada: afegir lògica gràfica a `engine` o `rules`, perquè trencaria la frontera arquitectònica establerta.

### Entrada per fases amb confirmació explícita

La selecció determinarà el context: robot actiu, casella de destí o blanc. El clic sobre una opció ressaltada enviarà l’acció; el final de fase es representarà amb un control visible. Els errors es conservaran com a missatge fins a la següent acció o canvi d’estat.

Alternativa descartada: moviment lliure basat en píxels, perquè permetria sol·licitar rutes que el motor no ha validat.

### Sprite i orientació

Els sprites es carregaran a partir de les rutes ja resoltes per `yaml_reader`; la UI aplicarà una transformació visual o indicador d’orientació sense alterar les dades del robot.

Alternativa descartada: codificar rutes relatives dins de la UI, perquè duplicaria la responsabilitat de configuració.

## Risks / Trade-offs

- [Diferències de resolució o escala] → usar mida d’hexàgon i origen configurables i limitar la selecció a la geometria calculada pel motor.
- [Pygame absent en entorns headless] → mantenir el motor i les proves sense finestra; fer les proves gràfiques amb superfície off-screen o mode dummy.
- [API de consulta insuficient] → afegir només adaptadors de lectura estables, sense traslladar regles a la UI.
- [Sprites amb proporcions diferents] → normalitzar-los dins del renderer i conservar la ruta/configuració com a font.

## Migration Plan

Afegir el punt d’entrada gràfic sense retirar el CLI. Verificar primer el mode headless i les proves del motor; després provar la finestra interactiva amb `config/example.yaml`. Si la UI falla, l’execució per consola continua sent el camí de recuperació.
