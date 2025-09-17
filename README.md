
# F1 Real‑Time Telemetry Demo (Prometheus + Grafana + Docker Swarm)

A lightweight, interview‑ready showcase that simulates race telemetry (speed, engine temp, lap time) and visualises it live in Grafana using Prometheus scraping. Designed to run on **Docker Swarm** (works on Docker Compose too).

## 📦 Stack
- **telemetry-sim** – Python Flask app exporting Prometheus metrics at `/metrics`
- **Prometheus** – scrapes every 2s, has an example alert rule
- **Grafana** – ready to import dashboard JSON

## 🗂 Structure
```
f1-telemetry-demo/
├─ docker-compose.yml
├─ prometheus/
│  ├─ prometheus.yml
│  └─ alerts.yml
├─ grafana/
│  └─ dashboards/
│     └─ f1-dashboard.json
└─ telemetry-sim/
   ├─ Dockerfile
   ├─ app.py
   └─ requirements.txt
```

## ▶️ Run (Local Compose)
```bash
docker compose up --build
# Prometheus: http://localhost:9090
# Grafana:    http://localhost:3000  (admin / admin)
# Metrics:    http://localhost:8000/metrics
```

## 🐝 Run (Docker Swarm)
```bash
docker swarm init                      # once per machine
docker stack deploy -c docker-compose.yml f1demo
```

## 📊 Import Dashboard
1. Open Grafana → Dashboards → Import
2. Upload `grafana/dashboards/f1-dashboard.json`
3. Set the Prometheus data source

## 🚨 Alerting
Prometheus has a sample alert (`EngineTooHot`) in `prometheus/alerts.yml`. Wire it to Alertmanager to route notifications.

## 🔧 Configuration
- Change driver count / update interval via env on `telemetry-sim` service:
  - `DRIVERS` (default 20)
  - `UPDATE_INTERVAL` (default 0.5s)
  - `JITTER` (randomness, default 0.2)

## 🧪 What to Demo
1. Open `/metrics` to show labelled driver metrics
2. Prometheus → **Status → Targets** (verify scrape OK)
3. Grafana → import dashboard → watch live updates
4. (Optional) Increase `JITTER=1` to spike temps/trigger alert

## 🛠 CI/CD: Build & Push Container Image
This repo includes a GitHub Actions workflow to build and push the `telemetry-sim` image to a registry.

### Option A: GitHub Container Registry (GHCR)
- Set **Repo → Settings → Secrets and variables → Actions → New repository secret**:
  - `GHCR_TOKEN` – a PAT with `write:packages`, `read:packages`
- Ensure your repo belongs to the user/org that owns the PAT.
- Update image name in `docker-compose.yml` if needed (`ghcr.io/<owner>/telemetry-sim:latest`).

### Option B: Docker Hub
- Set secrets:
  - `DOCKERHUB_USERNAME`
  - `DOCKERHUB_TOKEN` (create an Access Token in Docker Hub)
- Update `IMAGE_NAME: docker.io/<your-username>/telemetry-sim:latest` in the workflow.

## 🧷 License
MIT (or your preference)
