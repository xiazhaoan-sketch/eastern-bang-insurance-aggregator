# eastern-bang-insurance-aggregator

This repository hosts a Django project bootstrap for the Eastern Bang Insurance Aggregator.

## Getting Started

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The project entry point is `manage.py` and default settings live under `insurance_aggregator/settings.py`.

## Environment variables

The app reads configuration from the environment with sensible local defaults:

- `DJANGO_SECRET_KEY`: required in production.
- `DJANGO_DEBUG`: set to `False` for Render (`True` by default locally).
- `DJANGO_ALLOWED_HOSTS`: comma-separated hostnames. When unset, local hosts are used and Render falls back to `RENDER_EXTERNAL_HOSTNAME`.
- `DATABASE_URL`: SQLite by default; Render injects the Postgres URL automatically via `render.yaml`.

Copy `.env.example` to `.env` for local overrides if you are using a virtualenv.

## Deploying to Render.com

The repo includes a `Procfile` and a `render.yaml` blueprint. To deploy:

1. Push this repository to GitHub.
2. In Render, create a new Blueprint and point it at the repository.
3. Render provisions the Postgres database defined in `render.yaml`, installs dependencies, runs `collectstatic`, and applies migrations before every deploy.
4. Set `DJANGO_SECRET_KEY` to a strong value (Render will generate one automatically from the blueprint) and keep `DJANGO_DEBUG=False`.

The service starts with `gunicorn insurance_aggregator.wsgi:application` and serves static assets via Whitenoise. Collect static assets with `python manage.py collectstatic --noinput` before each deployment; this step is already part of the Render build command.
