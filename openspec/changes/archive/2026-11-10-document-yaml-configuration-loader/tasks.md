# Tasks

## 1. Contracte i model de configuració

- [x] 1.1 Definir els objectes interns per a mapa, posicions, objectius, equips, robots i regles; verificar que `load_config("config/example.yaml")` retorna una configuració completa.
- [x] 1.2 Fixar l’esquema estricte amb `schema_version: 1` i rebutjar camps desconeguts o obligatoris absents; verificar-ho amb tests de configuració invàlida.

## 2. Validació de mapa i entitats

- [x] 2.1 Validar dimensions `17 × 15`, elevacions, coordenades, identificadors i superposicions; verificar errors amb ruta del camp afectat.
- [x] 2.2 Validar exactament dos equips, orientacions, zones i valors positius de robots i regles; verificar el comportament amb configuracions invàlides.

## 3. Recursos i verificació

- [x] 3.1 Resoldre sprites respecte del directori del YAML i validar la signatura PNG; verificar rutes portables i sprites absents o invàlids.
- [x] 3.2 Afegir proves de càrrega i errors a `tests/test_yaml_reader.py` i executar `PYTHONPATH=src .venv/bin/pytest -q` amb resultat correcte.
- [x] 3.3 Registrar la fase completada a `docs/INDEX.md` i `docs/FASES_IMPLEMENTACIO.md`.

## Workflow follow-up

- Revisar els artefactes i arxivar el canvi quan la fase 1 quedi acceptada.
