PY=python
PORT?=8080
IMAGE?=ghcr.io/mostafiz93/virtual-diabetes-triage:v0.1

.PHONY: venv install train serve test docker-build docker-run fmt

venv:
	$(PY) -m venv .venv && . .venv/Scripts/activate

install:
	pip install -r requirements.txt

train:
	MODEL_VERSION=dev $(PY) -m ml.train --out-dir artifacts

serve:
	MODEL_DIR=artifacts uvicorn app.main:app --host 0.0.0.0 --port $(PORT)

test:
	PYTHONPATH=. pytest -q

docker-build:
	docker build -t $(IMAGE) .

docker-run:
	docker run --rm -p $(PORT):8080 $(IMAGE)
