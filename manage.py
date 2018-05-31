import csv
from wedding_site_backend.database import Invite
from wedding_site_backend.config import Config
from wedding_site_backend.manager import DBManager

def get_config():
    return Config()

def add_invite(passcode, session):
    new_invite = Invite(pass_code=passcode)
    new_invite.save(session)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('operation', help='operation to perform on database',
                        choices=['create', 'add_invite', 'add_from_file'])
    parser.add_argument('filename', help='Passphrase CSV file', nargs='?')
    parser.add_argument('passcodes', help='Pass codes for the invites', nargs='*')
    args = parser.parse_args()

    config = get_config()
    dbmanager = DBManager(config)
    if args.operation == 'create':
        dbmanager.create_database()
    elif args.operation == 'add_invite':
        for passcode in args.passcodes:
            add_invite(passcode, dbmanager.session)
    elif args.operation == 'add_from_file':
        with open(args.filename, 'r') as f:
            reader = csv.reader(f)
            for passcode in reader:
                add_invite(passcode[0], dbmanager.session)
