run:
	docker compose up --build

shell:
	docker compose exec web bash

test:
	docker compose run web pytest -vv

migrate:
	docker compose exec web python manage.py migrate
