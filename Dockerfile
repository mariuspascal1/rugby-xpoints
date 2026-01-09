FROM python:3.11-slim

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installer Poetry
RUN pip install poetry

# Copier les fichiers de dépendances
COPY pyproject.toml poetry.lock* ./

# Installer les dépendances
RUN poetry install --no-root

# Copier le code source
COPY . .

# Commande par défaut (peut être surchargée par docker compose)
CMD ["poetry", "run", "calcul_proba"]
