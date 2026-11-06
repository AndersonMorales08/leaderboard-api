# leaderboard-api

Una API chiquita en FastAPI: el ranking de puntos de un evento. Sin base de datos, todo en memoria.
Es uno de los repos del taller "Software factories with Claude Code".

## Preparar (antes del taller)

```zsh
gh repo fork sgomezahumada/leaderboard-api --clone && cd leaderboard-api
python3 -m venv venv && venv/bin/pip install -q -r requirements.txt
./doctor.sh          # hasta que diga "doctor: all green"
```

## En el taller

```zsh
./factory.sh 1       # el ticket #1 entra, sale un PR (o un PR [REJECTED])
```

Para ver la corrida en vivo, en otra terminal: `venv/bin/uvicorn dashboard.server:app --port 8001`
y abre http://127.0.0.1:8001.

Lo que tú cambias: `AGENTS.md` (el contexto), `gates/` (tus revisiones), `prompts/` (las fases).
Haz commit en `main` antes de cada corrida. Nada se mergea: los PRs son para comparar.
