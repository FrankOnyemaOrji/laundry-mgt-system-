from backend.API import create_app
from backend.API.utils import db
from backend.API.config.config import config_dict


def reset_database():
    app = create_app(config=config_dict["dev"])
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database has been reset.")


if __name__ == "__main__":
    reset_database()
