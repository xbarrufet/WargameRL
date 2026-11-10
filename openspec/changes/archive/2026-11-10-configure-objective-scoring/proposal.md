# Proposal

## Why

Els punts dels objectius estan escrits directament a la documentació i no es
poden ajustar per partida. A més, `DESCRIPCIO.md` i `DOCUMENT_TECNIC.md` tenen
valors diferents; la descripció funcional és la font de veritat i fixa els
valors per defecte en 1, 3 i 5 punts.

## What Changes

- Afegir al YAML una configuració de punts per a objectius de zona amiga,
  neutral i enemiga.
- Utilitzar aquesta configuració com a font de les regles de puntuació.
- Validar que els tres valors siguin enters no negatius i que els camps siguin
  obligatoris.
- Actualitzar `config/example.yaml` amb els valors `friendly: 1`, `neutral: 3`
  i `enemy: 5`.
- Corregir `DOCUMENT_TECNIC.md` perquè no contradigui `DESCRIPCIO.md` i remeti
  a aquesta com a font de les regles funcionals.
- Afegir proves de càrrega, validació i puntuació configurable.

## Capabilities

### New Capabilities

- `configurable-objective-scoring`: permet configurar els punts dels objectius
  segons la relació de la zona amb l’equip que puntua.

### Modified Capabilities

Cap.

## Impact

- Esquema YAML i `GameConfig` de `src/wargame/io/yaml_reader.py`.
- Futures regles de puntuació que consumiran aquests valors.
- Configuració d’exemple, documentació funcional/tècnica i tests.
- Les configuracions antigues sense el nou bloc de punts deixaran de ser vàlides
  (**BREAKING**), tret que es decideixi afegir compatibilitat per defecte.
