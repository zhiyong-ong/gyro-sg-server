MODULE = gyrosg
PORT = 8282

.PHONY: run-dev
run-dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port ${PORT}


.PHONY: clean
clean:
	rm -rf env
	python -m venv env


.PHONY: develop
develop:
	env/bin/pip install -r requirements.txt


.PHONY: requirements
requirements:
	env/bin/pip freeze > requirements.txt


.PHONY: format
format:
	env/bin/python -m black app tests

.PHONY: test
test:
	env/bin/python -m pytest tests


.PHONY: create-dev-db
create-dev-db:
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "CREATE DATABASE ${MODULE};"


.PHONY: clean-dev-db
clean-dev-db:
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "DROP DATABASE IF EXISTS ${MODULE};"
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "CREATE DATABASE ${MODULE};"


.PHONY: create-test-db
create-test-db:
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "CREATE DATABASE ${MODULE}_test;"


.PHONY: clean-test-db
clean-test-db:
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "DROP DATABASE IF EXISTS ${MODULE}_test;"
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "CREATE DATABASE ${MODULE}_test;"


.PHONY: create-migrations
create-migrations:
	@read -p "Enter a migration name for this migration: " MIGRATION_NAME; \
	GYROSG_API_ENV=dev alembic revision --autogenerate -m $$MIGRATION_NAME


.PHONY: migrate-dev
migrate-dev:
	GYROSG_API_ENV=dev alembic upgrade head
	env/bin/python -m app.initial_data


.PHONY: migrate-rollback
migrate-rollback:
	GYROSG_API_ENV=dev alembic downgrade -1


.PHONY: deploy
deploy:
	rsync -av -e 'ssh -p 18765' --exclude '.env' --exclude 'env' .  u1334-agpt8dlwwup4@gyrosg.com:~/gyrosg/server
