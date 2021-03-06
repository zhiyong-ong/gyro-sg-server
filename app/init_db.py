import logging

from app.db.initial_availabilities_data import initial_bike_availability_data
from app.db.initial_bike_data import initial_bike_data
from app.db.initial_licence_class_data import initial_licence_class_data
from app.db.initial_model_data import initial_model_data
from app.db.initial_transmission_data import initial_transmission_data
from app.db.initial_user_data import initial_user_data
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    initial_user_data(db)
    initial_model_data(db)
    initial_transmission_data(db)
    initial_licence_class_data(db)
    initial_bike_data(db)
    initial_bike_availability_data(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
