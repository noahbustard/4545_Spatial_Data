# Environment Setup — Missile Geometry 101

This assignment requires:

- Python 3.12.x
- pyenv
- virtual environment (.venv)

---

## First-Time Setup

From this assignment folder:

```bash
pyenv local 3.12.8
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
python -m ipykernel install --user \
  --name 4543-geo \
  --display-name "4543 Geo (.venv)"