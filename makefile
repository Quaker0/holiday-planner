.PHONY: serve

.venv:
	uv venv
	uv sync

test: .venv
	SECRET_KEY=dummy PYTHONPATH=./src uv run pytest src/

serve:
	docker-compose up --build

# Make sure to 'make serve' in another tab for these commands 👇

setup-db:
	docker compose exec web uv run python manage.py migrate

load-dummy-data:
	docker compose exec web uv run python manage.py load_dummy_data

serve-terminal:
	docker compose exec web sh
	
smoke-tests:
	SECRET_KEY=dummy PYTHONPATH=./src uv run pytest smoke_tests/