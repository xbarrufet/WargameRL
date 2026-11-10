# Design

## Context

La fase 1 ja disposa d’un carregador a `src/wargame/io/yaml_reader.py`, una
configuració d’exemple i proves de càrrega i errors. La implementació no ha de
dependre de Pygame i les rutes de recursos han de ser portables amb el YAML.

## Goals / Non-Goals

**Goals:**

- Mantenir un contracte explícit per a la configuració YAML.
- Validar tota la configuració abans de construir el resultat intern.
- Fer localitzables els errors mitjançant rutes de camps.
- Reutilitzar la documentació funcional, tècnica i de fases sense duplicar-la.

**Non-Goals:**

- Implementar el model de dades de la partida de la fase 2.
- Implementar regles de moviment, combat, UI o RL.
- Canviar el format de `config/example.yaml`.

## Decisions

- **Spec separada `yaml-configuration`:** és una capacitat coherent i podrà
  evolucionar independentment del model de dades.
- **Esquema estricte:** els camps desconeguts es rebutgen per evitar errors
  silenciosos; l’alternativa seria tolerar-los i perdre detecció de typos.
- **Rutes relatives al YAML:** permeten moure la configuració i els seus
  recursos com una unitat; l’alternativa de fer-les relatives al directori de
  treball faria l’execució dependent de l’entorn.
- **Model intern immutable:** les dades carregades es representen amb objectes
  immutables, cosa que evita modificar accidentalment la configuració validada.
- **Validació de signatura PNG:** es valida el format PNG sense inicialitzar la
  UI; la càrrega gràfica queda fora de la responsabilitat del lector.

## Risks / Trade-offs

- [Risk] La validació de signatura PNG no comprova que la imatge sigui
  visualment renderitzable per Pygame → la UI haurà de fer la seva validació de
  càrrega quan s’implementi.
- [Risk] L’esquema estricte pot rebutjar extensions futures → caldrà versionar
  explícitament l’esquema abans d’afegir camps.

## Migration Plan

No cal migració: la configuració existent ja compleix l’esquema. En canviar el
format, s’haurà d’incrementar `schema_version` i actualitzar aquesta spec.
