import csv
from wedding_site_backend.database import get_engine, base, Invite, start_session
from wedding_site_backend.config import Config

def get_config():
    return Config()

def create_table(config):
    base.metadata.create_all(get_engine(config))

def add_invite(passcode, session):
    new_invite = Invite(pass_code=passcode)
    session.add(new_invite)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('operation', help='operation to perform on database',
                        choices=['create', 'add_invite', 'add_from_file'])
    parser.add_argument('filename', help='Passphrase CSV file', nargs='?')
    parser.add_argument('passcodes', help='Pass codes for the invites', nargs='*')
    args = parser.parse_args()

    config = get_config()
    if args.operation == 'create':
        create_table(config)
    elif args.operation == 'add_invite':
        session = start_session(config)
        for passcode in args.passcodes:
            add_invite(passcode, session)
        session.commit()
    elif args.operation == 'add_from_file':
        session = start_session(config)
        with open(args.filename, 'r') as f:
            reader = csv.reader(f)
            for passcode in reader:
                add_invite(passcode[0], session)
            session.commit()
