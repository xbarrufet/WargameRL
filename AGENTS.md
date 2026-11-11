## Project Documentation

The following documents define the project:

- `/docs/DESCRIPCIO.md`: Project vision, objectives, architecture, and scope.
- `/docs/GAME_RULES.md`: Authoritative definition of game mechanics, rules, and configurable parameters.
- `openspec/specs/`: Accepted specifications describing implemented or expected system behavior.

### Source of Truth

- `/docs/GAME_RULES.md` is authoritative for game design decisions.
- OpenSpec specifications define the expected implementation behavior.
- YAML files provide runtime configuration values and must respect the game rules.
- `/docs/DESCRIPCIO.md` defines project scope and architectural boundaries.

### Development Guidelines

Before implementing or modifying game mechanics:

1. Read `/docs/GAME_RULES.md`.
2. Review the relevant OpenSpec specifications.
3. Identify inconsistencies between the game rules and existing specifications.
4. Do not invent or change game rules without explicit approval.
5. Use the OpenSpec change workflow for modifications affecting system behavior.
6. Keep implementation, tests, and specifications consistent with the approved rules.

### AI Architecture

Maintain a strict separation between:

- **Game Engine:** Game state, rules, commands, validation, and resolution.
- **Micro AI:** Scripted tactical execution using heuristics and heatmaps.
- **Macro AI:** Reinforcement Learning policy responsible for high-level tactical decisions.

The Game Engine must not depend on either AI implementation or the graphical interface.