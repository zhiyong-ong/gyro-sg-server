MODULE = gyrosg
include .env

################
# DEV COMMANDS #
################

.PHONY: run-dev
run-dev:
	env/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port ${SERVER_PORT}


.PHONY: clean
clean:
	rm -rf env || true
	python3 -m venv env


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
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "CREATE DATABASE ${DB_NAME};"
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "CREATE DATABASE ${MODULE}_test;"


.PHONY: clean-dev-db
clean-dev-db:
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "DROP DATABASE IF EXISTS ${DB_NAME};"
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "CREATE DATABASE ${DB_NAME};"


.PHONY: clean-test-db
clean-test-db:
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "DROP DATABASE IF EXISTS ${MODULE}_test;"
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "CREATE DATABASE ${MODULE}_test;"


.PHONY: create-migrations
create-migrations:
	@read -p "Enter a migration name for this migration: " MIGRATION_NAME; \
	GYROSG_API_ENV=dev env/bin/python -m alembic revision --autogenerate -m $$MIGRATION_NAME


.PHONY: migrate-dev
migrate-dev:
	GYROSG_API_ENV=dev env/bin/python -m alembic upgrade head


.PHONY: migrate-rollback
migrate-rollback:
	GYROSG_API_ENV=dev env/bin/python -m alembic downgrade -1


.PHONY: init-dev-db
init-dev-db: migrate-dev
	env/bin/python -m app.init_db


.PHONY: deploy-dev
deploy-dev:
	rsync -av -e 'ssh -i ~/.ssh/gyrosg-server.pem' --exclude '.env' --exclude 'env' --exclude '.git*' --exclude '.idea*' --exclude 'tests' .	\
	ubuntu@gyrosg-api.com:~/gyrosg/dev/server


#################
# PROD COMMANDS #
#################

.PHONY: deploy-prod
deploy-prod:
	rsync -av -e 'ssh -i ~/.ssh/gyrosg-server.pem' --exclude '.env' --exclude 'env' --exclude '.git*' --exclude '.idea*' --exclude 'tests' .	\
	ubuntu@gyrosg-api.com:~/gyrosg/server


.PHONY: create-prod-db
create-prod-db:
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "CREATE DATABASE ${DB_NAME};"


.PHONY: migrate-prod
migrate-prod:
	GYROSG_API_ENV=prod env/bin/python -m alembic upgrade head


.PHONY: clean-prod-db
clean-prod-db:
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "DROP DATABASE IF EXISTS ${DB_NAME};"
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "CREATE DATABASE ${MODULE};"


.PHONY: init-prod-db
init-prod-db: migrate-prod
	env/bin/python -m app.init_db