# Índex de WargameRL

## Estat actual

Fase activa: **Fase 2 — Model de dades**.

L’entorn Python del projecte és el virtualenv `.venv`. La fase 0 està
completades: estructura de paquets, `pyproject.toml`, dependències bàsiques,
punt d’entrada i carregador/validador YAML. Les proves actuals s’executen
correctament.

## Documentació principal

- [Descripció funcional](./DESCRIPCIO.md): regles del joc i components inicials.
- [Document tècnic](./DOCUMENT_TECNIC.md): arquitectura, model de dades i
  tecnologia proposada.
- [Fases d’implementació](./FASES_IMPLEMENTACIO.md): ordre de treball i
  lliuraments.

## Configuració i recursos

- [Configuració YAML de prova](../config/example.yaml)
- [Imatges dels robots](../config/imgs/)

## Estructura de codi

```text
src/wargame/
├── model/    # Entitats i estat de la partida
├── rules/    # Regles de moviment, combat i puntuació
├── engine/   # Execució i validació d’accions
├── io/       # Lectura i validació de configuració
└── ui/       # Visualització Pygame
```

## Ordre de consulta recomanat

1. Llegir aquest índex.
2. Consultar només la fase activa a `FASES_IMPLEMENTACIO.md`.
3. Consultar `DOCUMENT_TECNIC.md` per a decisions d’arquitectura.
4. Consultar `DESCRIPCIO.md` només per confirmar regles funcionals.

## Regla de manteniment

`DESCRIPCIO.md` és la font de les regles funcionals, `DOCUMENT_TECNIC.md` és
la font de l’arquitectura i `FASES_IMPLEMENTACIO.md` és la font de l’ordre de
treball. No s’han de duplicar decisions entre aquests documents.
