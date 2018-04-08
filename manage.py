from wedding_site_backend import database

if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('operation', help='operation to perform on database',
                      choices=['create'])
  args = parser.parse_args()

  if args.operation == 'create':
    database.base.metadata.create_all(database.get_engine())
