# Proposal

## Why

La fase 1 ja està implementada, però el contracte del carregador YAML només és
localitzable dins de la documentació general i del codi. Registrar-lo com una
spec d’OpenSpec permetrà reutilitzar-lo com a font de requisits quan es
desenvolupin el model de dades, les eines de consola i les proves futures.

## What Changes

- Documentar el comportament observable del carregador i validador YAML.
- Fixar l’esquema de configuració, les validacions i el model retornat.
- Registrar les decisions preses: rutes de sprites relatives al YAML, camps
  desconeguts rebutjats, errors amb ruta del camp i `schema_version: 1`.
- Enllaçar la spec amb la implementació, els tests i la documentació existent.

## Capabilities

### New Capabilities

- `yaml-configuration`: càrrega, validació i conversió d’una configuració YAML
  en un objecte intern segur.

### Modified Capabilities

Cap.

## Impact

- Documentació OpenSpec sota aquest canvi.
- Implementació existent a `src/wargame/io/yaml_reader.py`.
- Tests a `tests/test_yaml_reader.py`.
- Configuració d’exemple a `config/example.yaml` i documentació de projecte a
  `docs/DESCRIPCIO.md`, `docs/DOCUMENT_TECNIC.md` i
  `docs/FASES_IMPLEMENTACIO.md`.
- No s’introdueixen canvis de runtime ni dependències noves.
