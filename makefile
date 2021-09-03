MODULE = gyrosg
PORT = 30009


################
# DEV COMMANDS #
################

.PHONY: run-dev
run-dev:
	env/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port ${PORT}


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
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "CREATE DATABASE ${MODULE};"
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "CREATE DATABASE ${MODULE}_test;"


.PHONY: clean-dev-db
clean-dev-db:
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "DROP DATABASE IF EXISTS ${MODULE};"
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "CREATE DATABASE ${MODULE};"


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


.PHONY: migrate-rollback
migrate-rollback:
	GYROSG_API_ENV=dev alembic downgrade -1


.PHONY: init-data
init-data:
	env/bin/python -m app.init_db


.PHONY: deploy
deploy:
	rsync -av -e 'ssh -i ~/.ssh/gyrosg-server.pem' --exclude '.env' --exclude 'env' --exclude '.git*' --exclude '.idea*' --exclude 'tests' .	\
	ec2-user@ec2-54-254-7-97.ap-southeast-1.compute.amazonaws.com:~/gyrosg/server


#################
# PROD COMMANDS #
#################

.PHONY: create-prod-db
create-prod-db:
	PGPASSWORD=gyrosg psql postgres -U gyrosg -h localhost -c "CREATE DATABASE ${MODULE};"

.PHONY: migrate-prod
migrate-prod:
	GYROSG_API_ENV=prod env/bin/python -m alembic upgrade head


.PHONY: init-prod-data
init-prod-data:
	env/bin/python -m app.init_db
