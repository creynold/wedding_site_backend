import configparser
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from wedding_site_backend import database

def get_engine():
  config = configparser.ConfigParser(allow_no_value=True)
  config.read('wedding_site_backend/config.ini')

  return create_engine(
      URL(config['database']['database_dialect'], **config['database_url']),
      echo=True)

if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('operation', help='operation to perform on database',
                      choices=['create'])
  args = parser.parse_args()

  if args.operation == 'create':
    database.base.metadata.create_all(get_engine())
