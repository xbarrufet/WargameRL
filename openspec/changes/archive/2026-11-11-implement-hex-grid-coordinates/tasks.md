# Tasks

## 1. Geometria de coordenades

- [x] 1.1 Implementar els sis vectors de veïnatge axial i una funció de veïns que filtri les coordenades fora del tauler; verificar-ho amb tests per a una casella interior i una de frontera.
- [x] 1.2 Implementar la distància hexagonal axial; verificar identitat, veïns a distància 1 i una distància multicasella.
- [x] 1.3 Afegir validació reutilitzable de coordenades i consulta d’elevació a `Board`; verificar els errors de límit i els valors 0/1.

## 2. Ocupació i integració amb l’estat

- [x] 2.1 Exposar la consulta de casella ocupada a partir de les posicions dels robots; verificar caselles lliures, ocupades i robots destruïts.
- [x] 2.2 Mantenir la serialització existent de coordenades i executar els tests de `GameState` i de configuració per verificar que no hi ha regressions.

## 3. Conversió flat-top

- [x] 3.1 Implementar la projecció coordenada → centre de pantalla amb mida i origen configurables; verificar els centres coneguts amb tolerància numèrica.
- [x] 3.2 Implementar la conversió pantalla → coordenada amb arrodoniment axial/cúbic i comprovació geomètrica del polígon; verificar round trips, fronteres i punts fora del tauler.
- [x] 3.3 Documentar la fórmula flat-top i la relació amb l’orientació `N` a `docs/DOCUMENT_TECNIC.md` i `docs/FASES_IMPLEMENTACIO.md`; verificar que la documentació no contradigui `docs/GAME_RULES.md`.

## 4. Integració

- [x] 4.1 Executar la suite completa amb `pytest` i validar l’OpenSpec amb `openspec validate --changes --strict --no-interactive`.
