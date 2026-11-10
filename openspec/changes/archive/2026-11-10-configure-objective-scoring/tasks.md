# Tasks

## 1. Esquema i validació YAML

- [x] 1.1 Afegir `rules.objective_points` amb `friendly`, `neutral` i `enemy` a `config/example.yaml` i `GameConfig`; verificar que els valors 1/3/5 es carreguen.
- [x] 1.2 Validar que les tres claus existeixen i contenen enters no negatius; afegir tests per camps absents, textos, decimals i valors negatius.

## 2. Regles i documentació

- [x] 2.1 Exposar els punts configurats perquè la futura resolució de puntuació distingeixi zona amiga, neutral i enemiga; verificar els tres casos amb tests de regla.
- [x] 2.2 Actualitzar `DESCRIPCIO.md` i `DOCUMENT_TECNIC.md` perquè la semàntica i els valors siguin coherents i la descripció funcional sigui la font de veritat; verificar que no queda cap referència 1/2/4.

## 3. Integració

- [x] 3.1 Actualitzar tests i executar `PYTHONPATH=src .venv/bin/pytest -q` sense regressions.
- [x] 3.2 Executar `openspec validate --changes --strict --no-interactive` i verificar que el canvi queda preparat per aplicar.
