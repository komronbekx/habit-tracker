

setup:
	uv run python manage.py makemigrations
	uv run python manage.py migrate
	uv run python manage.py createsuperuser
	uv run python manage.py createcachetable

seed:
	uv run python manage.py shell -c "import scripts.seed"

up:
	docker compose -f docker/docker-compose.yml up -d --build

down:
	docker compose -f docker/docker-compose.yml down

logs:
	docker compose -f docker/docker-compose.yml logs -f

shell:
	docker compose -f docker/docker-compose.yml exec web bash

migrate:
	docker compose -f docker/docker-compose.yml exec web uv run python manage.py migrate

superuser:
	docker compose -f docker/docker-compose.yml exec web uv run python manage.py createsuperuser

dev:
	uv run python manage.py runserver 0.0.0.0:8000

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy .

test:
	uv run python manage.py test

migrations:
	uv run python manage.py makemigrations
	uv run python manage.py migrate

check-migration:
	uv run python manage.py makemigrations --check --dry-run

ci: lint format typecheck test check-migration