# Tasks

## 1. Tipus i entitats del domini

- [x] 1.1 Definir `HexCoordinate`, `Direction` i `Phase`, incloent els valors vàlids; verificar-ho amb tests de construcció i serialització.
- [x] 1.2 Definir `Team`, `Robot`, `Objective` i `Board` amb les dades necessàries de `GameConfig`; verificar que les entitats conserven els valors del YAML.

## 2. Estat inicial de la partida

- [x] 2.1 Implementar `GameState` amb equip actiu, ronda, torn, fase, puntuacions, resultat i llavor opcional; verificar els valors inicials deterministes.
- [x] 2.2 Construir un `GameState` complet a partir de `GameConfig` sense modificar la configuració d’origen; verificar-lo amb `config/example.yaml`.
- [x] 2.3 Validar els invariants del model i rebutjar entrades incompletes sense retornar estats parcials; verificar els errors amb tests dedicats.

## 3. Serialització i verificació

- [x] 3.1 Implementar serialització i deserialització JSON-compatible de l’estat complet; verificar un round trip equivalent.
- [x] 3.2 Afegir tests de model, estat inicial i serialització, i executar `PYTHONPATH=src .venv/bin/pytest -q` sense regressions.

## Workflow follow-up

- Revisar els artefactes i iniciar `$openspec-apply-change` quan es vulgui implementar la fase 2.
