# WargameRL

Prototip de simulació d’un wargame tàctic per torns entre dos equips de
robots, amb una futura extensió per a aprenentatge per reforç (RL).

El projecte separa el motor de joc de la interfície gràfica i de l’adaptador
RL futur. Això permet provar les regles i executar simulacions sense dependre
de Pygame.

## Estat del projecte

El projecte es troba en la **fase 0 — preparació**. Actualment inclou:

- estructura de paquets Python sota `src/wargame/`;
- configuració de paquet amb `pyproject.toml`;
- CLI inicial (`wargame`);
- configuració d’exemple del mapa a `config/example.yaml`;
- prova smoke amb `pytest`.

El motor de simulació, el carregador YAML, les regles, la UI i l’adaptador RL
s’implementaran en les fases següents.

## Requisits

- Python 3.11 o superior
- `pip` i `venv`

Les dependències principals són `PyYAML` i `pygame-ce`. Les eines de
desenvolupament inclouen `pytest`.

## Instal·lació per desenvolupar

```bash
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Ús actual

Consultar la versió instal·lada:

```bash
wargame --version
```

Executar la CLI inicial:

```bash
wargame
```

En aquesta fase la CLI només confirma que el punt d’entrada està preparat;
la partida encara no s’executa.

## Tests

```bash
pytest
```

## Arquitectura prevista

```text
Configuració YAML → Motor de simulació → Visualització Pygame
                                      ↘ Adaptador RL futur
```

```text
src/wargame/
├── model/    # Estat i entitats de la partida
├── rules/    # Moviment, combat, visibilitat i puntuació
├── engine/   # Accions, fases i validació
├── io/       # Lectura i validació YAML
└── ui/       # Visualització Pygame
```

El motor serà la font única de veritat. La UI no modificarà directament
l’estat: enviarà accions al motor, que les validarà i les aplicarà.

## Joc previst

La partida es juga sobre una graella hexagonal de `17 × 15` caselles, amb dos
equips de robots i tres fases per torn:

1. moviment;
2. dispar;
3. puntuació.

La configuració d’exemple inclou elevacions, objectius, robots, orientacions i
sprites. Les regles detallades es troben a [docs/DESCRIPCIO.md](docs/DESCRIPCIO.md)
i les decisions d’arquitectura a [docs/DOCUMENT_TECNIC.md](docs/DOCUMENT_TECNIC.md).

## Documentació

- [Índex de documentació](docs/INDEX.md)
- [Descripció funcional i regles](docs/DESCRIPCIO.md)
- [Document tècnic](docs/DOCUMENT_TECNIC.md)
- [Fases d’implementació](docs/FASES_IMPLEMENTACIO.md)
- [Configuració YAML d’exemple](config/example.yaml)

## Contribució

Abans d’obrir un canvi, executa:

```bash
pytest
```

Mantén la separació entre el motor, les regles i la UI, i actualitza la
documentació corresponent quan canviï el comportament del joc.

