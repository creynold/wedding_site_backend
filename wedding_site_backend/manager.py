from sqlalchemy import create_engine
from sqlalchemy import orm
from sqlalchemy.orm import scoping

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
