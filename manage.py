from wedding_site_backend.database import get_engine, base
from wedding_site_backend.config import Config

if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('operation', help='operation to perform on database',
                      choices=['create'])
  args = parser.parse_args()

  config = Config()
  if args.operation == 'create':
    base.metadata.create_all(get_engine(config))
