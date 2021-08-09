import logging

from app.db.initial_bike_data import initial_bike_data
from app.db.initial_model_data import initial_model_data
from app.db.initial_user_data import initial_user_data
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    initial_user_data(db)
    initial_model_data(db)
    initial_bike_data(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
