# FromChat Backend — API Server

[Читать на других языках: Русский](./README.md)

<div align="center">
  <img src="https://raw.githubusercontent.com/fromchat-messenger/android/main/app/android/src/main/ic_launcher-playstore.png" width="120" alt="FromChat Logo" />

  **API server for FromChat messenger**

  [🖥️ Backend](https://github.com/fromchat-messenger/backend) • [🌐 Web Client](https://github.com/fromchat-messenger/web) • [📱 Android](https://github.com/fromchat-messenger/android) • [🌍 Website](https://github.com/fromchat-messenger/site)
</div>

---

## 📝 Description

Python/FastAPI backend for FromChat clients (Android, Web, iOS). Multiple Docker services: public API, messaging, file storage, LiveKit, PostgreSQL. Production edge is Caddy + HAProxy (`compose.prod.yml`).

---

## 📊 Client Comparison

| Feature | Android | Web | iOS |
|---|---|---|---|
| **Messaging & profiles** | ✅ | ✅ | ❌ |
| **Voice/video calls** | ✅ | ✅ | ❌ |
| **Screen sharing** | ✅ | ✅ | ❌ |
| **Message reactions** | ❌ | ✅ | ❌ |
| **Rich attachment support** | ✅ | ❌ | ❌ |

---

## 🏗️ Architecture

| Service | Port (dev) | Network | Purpose |
|---|---|---|---|
| **backend** (main) | 8300 | public + services | Public API, auth, profiles, WebSocket |
| **messaging** | 8301 | services | Internal — messages |
| **file_storage** | 8302 | services | Internal — files |
| **livekit** | 8303 / 8304 (+ UDP) | public | Calls |
| **postgres** | 127.0.0.1:5432 | services | Database |
| **caddy** + **haproxy** | 80/443 (prod) | — | TLS / reverse proxy (`compose.prod.yml`) |

- `public` — reachable from outside (main, livekit, …)
- `services` — stack-internal only (messaging, file_storage, postgres)

---

## 🔧 Stack

| Component | Role |
|---|---|
| Python | 3.12+ |
| FastAPI | API |
| PostgreSQL | DB (per-service DBs/users) |
| SQLAlchemy 2 + Alembic | ORM & migrations |
| Docker Compose | orchestration |
| LiveKit | calls |
| Caddy + HAProxy | production edge |

---

## 🔒 Security

- Legal server-side message encryption + compliance keys
- JWT
- HTTPS in production
- Rate limiting (slowapi)
- Messaging / file storage are not published externally
- Firebase / Web Push (VAPID) — optional

---

## 📥 Running

### Requirements

- Docker 20.10+ and Compose plugin
- Python 3.12+ and npm (local scripts / `.env` generation)
- ~2 GB RAM, ~10 GB disk

### 1. Clone

```bash
git clone https://github.com/fromchat-messenger/backend.git
cd backend
```

### 2. Generate `.env`

There is no `.env.example` — use the generator:

```bash
npm install                 # venv + pip install -r requirements.txt
npm run generate:env        # scripts/generate:env.sh (interactive)
```

Typical keys: `JWT_SECRET`, `COMPLIANCE_PUBLIC_KEY`, Postgres passwords (`POSTGRES_PASSWORD`, `MAIN_DB_PASSWORD`, …), `LIVEKIT_*`, `MESSAGE_RETENTION_DAYS`, VAPID, optional `RELEASES_TOKEN` / Firebase.

Also writes `compliance_keypair.txt` — **keep the private key offline**.

### 3. Start the stack

```bash
npm run docker:up
# equivalent:
docker compose --env-file .env -f compose.yml up --build
```

Tear down (including volumes):

```bash
npm run docker:down
```

### 4. Verify

```bash
curl http://localhost:8300/health
# {"status":"healthy","service":"main"}
```

Swagger: `http://localhost:8300/docs`  
ReDoc: `http://localhost:8300/redoc`

The web client in dev proxies the backend as `/api` → this `:8300` port.

### Production edge

```bash
docker compose --env-file .env -f compose.yml -f compose.prod.yml up -d
```

One-click / published stack: [deployment](https://github.com/fromchat-messenger/deployment).

### Firebase (optional)

Place `firebase-cert.json` in the repo root (compose mounts it into the main container).

---

## 🔧 Local development (main only, no Docker)

Prefer Docker for the full stack. Main API alone:

```bash
npm install
npm run generate:env   # if .env is missing
npm run livekit:ensure # if you need calls
npm run dev            # uvicorn src.main.main:app on :8300 --reload
```

Messaging and file_storage still need to be started separately (usually via Compose).

Migrations run when Docker images start; for manual runs use Alembic from the container / venv for the relevant service.

---

## 🛠 Troubleshooting

```bash
docker compose --env-file .env -f compose.yml logs -f backend
docker compose --env-file .env -f compose.yml ps
lsof -i :8300
```

Database issues:

```bash
docker compose --env-file .env -f compose.yml exec postgres \
  psql -U postgres -c "SELECT 1"
# full data reset (destructive):
docker compose --env-file .env -f compose.yml down -v
```

---

## 🤝 Contributing

1. Branch for your change
2. PR with a description
3. Confirm the stack starts (`npm run docker:up`) and `/health` responds

---

## 📄 License

Distributed under the GNU Affero General Public License v3.0 (same as other FromChat repos).

---

## 🔗 Related Repositories

- [Web Client](https://github.com/fromchat-messenger/web)
- [Android Client](https://github.com/fromchat-messenger/android)
- [Website](https://github.com/fromchat-messenger/site)
- [Deployment](https://github.com/fromchat-messenger/deployment)
- [Updater](https://github.com/fromchat-messenger/updater)

---

## 📞 Support

- 💬 Telegram: https://t.me/fromchat_community
- 🐛 Issues: GitHub Issues on the relevant repo

---

**[⬆ back to top](#fromchat-backend--api-server)**
