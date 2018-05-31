from sqlalchemy import create_engine
from sqlalchemy import orm
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoping

from .database import BaseModel

class DBManager(object):
    def __init__(self, config):
        self.config = config

        self.engine = create_engine(
          URL(config.get('database', 'database_dialect'),
              **config.get_group('database_url')),
          echo=True)

        self.DBSession = scoping.scoped_session(
            orm.sessionmaker(
                bind=self.engine,
                autocommit=True
            )
        )

    @property
    def session(self):
        return self.DBSession()

    def create_database(self):
        BaseModel.metadata.create_all(self.engine)
