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
