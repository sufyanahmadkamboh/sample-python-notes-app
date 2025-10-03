# Mini Notes (Python-only)

A tiny Flask + SQLite web app you can use to **learn, practice, and teach deployment** of a Python project.

## What it does
- List notes
- Add a note
- Delete a note
- Data stored in a local `SQLite` file (`notes.db`)

---

## 1) Run locally (Windows/Mac/Linux)

```bash
# 1) Get the code
unzip python-only-mini-notes.zip
cd python-only-mini-notes

# 2) Create & activate a virtual env (recommended)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Install deps
pip install -r requirements.txt

# 4) Start the app (dev mode)
python app.py
# Open http://localhost:5000
```

> The first run will create `notes.db` automatically.

---

## 2) Run with Gunicorn (production-style, no Docker)
```bash
pip install -r requirements.txt
# Linux/macOS
gunicorn app:app -w 2 -b 0.0.0.0:5000
```

---

## 3) Run with Docker
```bash
# Build
docker build -t mini-notes:latest .

# Run
docker run -p 5000:5000 mini-notes:latest
# Open http://localhost:5000
```

**Teach points:**
- `Dockerfile` installs dependencies and starts Gunicorn.
- Port mapping `-p 5000:5000` publishes the app.

---

## 4) Deploy to a Linux VM (Ubuntu example)

```bash
# Update system, install Python + venv
sudo apt update && sudo apt install -y python3-pip python3-venv

# Create app folder
mkdir -p /opt/mini-notes && cd /opt/mini-notes

# Copy project files to server (use scp or sftp from your machine)

# Create venv and install deps
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Test run with Gunicorn
gunicorn app:app -w 2 -b 0.0.0.0:5000
```

(Optional) Create a **systemd service** so it starts on boot:
```ini
# /etc/systemd/system/mini-notes.service
[Unit]
Description=Mini Notes Flask app
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/mini-notes
Environment="PATH=/opt/mini-notes/.venv/bin"
ExecStart=/opt/mini-notes/.venv/bin/gunicorn -w 2 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable mini-notes
sudo systemctl start mini-notes
```

Optionally place Nginx/Apache in front as a reverse proxy (TLS, domain).

---

## 5) Quick deploy to platforms (no server admin)

- **Render / Railway / Fly.io / Azure App Service / Google Cloud Run / AWS App Runner** all work well.
- Use this repo as the source. Most platforms detect `Python` automatically.
- If a `PORT` env var is provided by the platform, `Procfile` shows how to run: `web: gunicorn app:app -w 2 -b 0.0.0.0:$PORT`.

---

## 6) Project structure

```
python-only-mini-notes/
├── app.py
├── requirements.txt
├── Dockerfile
├── Procfile
├── templates/
│   ├── base.html
│   └── index.html
└── static/
    └── styles.css
```

---

## 7) Next steps (practice ideas)
- Add an **edit** feature for notes
- Add a **login** page (Flask-Login)
- Add a **/health** endpoint for probes
- Swap SQLite for **PostgreSQL** and use **SQLAlchemy**
- Add **unit tests** and **CI/CD** (GitHub Actions)
- Container scan + deploy to **Kubernetes** (microk8s/minikube)

Happy teaching! 🎓
# sample-python-notes-app
