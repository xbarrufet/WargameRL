# Design

## Context

El punt d’entrada actual només implementa `--version`; el motor ja exposa `GameState`, accions de moviment, dispar i final de fase, així com els resultats de puntuació i final. La implementació ha de respectar `docs/GAME_RULES.md`, mantenir el motor independent de la UI i usar el carregador YAML existent.

## Goals / Non-Goals

**Goals:**

- Proporcionar una ordre de simulació de prova executable des de la consola.
- Proporcionar un bucle manual senzill amb una gramàtica d’accions documentada.
- Centralitzar el format de sortida perquè les proves puguin comprovar esdeveniments importants.
- Fer que la llavor controli tota la resolució aleatòria del motor.
- Cobrir càrrega, execució, errors, tancament per punts i límit de rondes amb proves d’integració.

**Non-Goals:**

- No afegir regles ni modificar la resolució del motor.
- No construir la UI Pygame ni un protocol estable per a tercers.
- No introduir encara l’adaptador Gymnasium o una política d’IA.

## Decisions

### CLI amb subcomandes i opcions explícites

Afegir una subcomanda `simulate` amb `--config`, `--seed`, `--mode {demo,manual}` i una opció de seqüència només si cal per fer les proves. La ruta per defecte es resol relativa a l’arrel del projecte o al paquet de manera determinista. Es manté `--version` i el comportament d’errors d’`argparse`.

Alternativa descartada: substituir l’ordre actual per un script separat; faria més difícil validar el punt d’entrada instal·lat.

### Adaptador de consola separat del motor

Crear un mòdul de presentació/orquestració sota `wargame` que transformi línies d’entrada en accions del motor i formati snapshots i resultats. La seqüència demo només compon accions existents (`execute_movement`, `execute_shot`, `execute_end_phase`) i no reimplementa càlculs de control o victòria.

Alternativa descartada: posar `print()` i parsing dins de `engine`; violaria la separació d’arquitectura i complicaria la futura UI.

### Sortida textual estable i orientada a esdeveniments

Cada execució imprimirà una capçalera amb configuració i llavor, un snapshot inicial amb la posició i l’estat de cada robot, línies per transició/acció, resums de combat, puntuació després de `SCORING` i un bloc final amb causa, puntuacions i `GameResult`. Els errors de dades o arguments aniran a stderr i els errors d’una acció manual no mutaran l’estat ni tancaran el procés.

Alternativa descartada: serialitzar sempre tot `GameState` com a JSON; és útil per depuració però massa sorollós per al flux interactiu i no substitueix els missatges humans.

### Mode manual amb gramàtica mínima

El mode manual acceptarà ordres textuals per finalitzar fase i executar les accions ja disponibles, amb `help` i `quit`. El parser validarà només la forma de l’ordre; el motor decidirà si l’acció és legal. La sintaxi exacta es cobrirà amb proves i ajuda del CLI, sense convertir-la en una API persistent.

## Risks / Trade-offs

- [Risk] La seqüència demo pot dependre de l’escenari actual → Mitigació: construir-la a partir de consultes d’accions accessibles i provar-la amb `config/example.yaml`.
- [Risk] La sortida humana pot canviar accidentalment → Mitigació: centralitzar els formatters i comprovar fragments/ordres en proves CLI, sense acoblar-ho a representacions internes.
- [Risk] Una llavor només és reproduïble si totes les tirades passen pel generador del motor → Mitigació: no generar daus a la capa de consola i afegir una prova de dues execucions equivalents.
- [Risk] El mode manual pot quedar bloquejat en entrada interactiva durant CI → Mitigació: mantenir el mode demo no interactiu i injectar `stdin`/`stdout` a les proves.

## Migration Plan

No hi ha migració de dades. Afegir la subcomanda mantenint `wargame --version`; verificar primer el mode demo i després el manual. Si cal revertir, retirar el mòdul de consola i la subcomanda sense tocar els estats serialitzats ni les regles.
