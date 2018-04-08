import configparser
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from wedding_site_backend import database

config = configparser.ConfigParser(allow_no_value=True)
config.read('wedding_site_backend/config.ini')

engine = create_engine(
    URL(config['database']['database_dialect'], **config['database_url']),
    echo=True)

database.base.metadata.create_all(engine)
