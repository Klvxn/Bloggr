import os
from pathlib import Path


base_dir = Path(__file__).resolve().parent
BOOTSTRAP_BOOTSWATCH_THEME = "zephyr"
DATABASE = "database/bloggr.db"
ENV = "development"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{Path(base_dir).joinpath(DATABASE)}"
SECRET_KEY = "safe-space"
