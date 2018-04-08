import configparser
from sqlalchemy import Column, String, ForeignKey, Integer, create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.schema import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

base = declarative_base()

song_requests = Table(
    'song_requests', base.metadata,
    Column('invite_id', String, ForeignKey('invite.pass_code')),
    Column('song_id', Integer, ForeignKey('song.id'))
)

class Invite(base):
    __tablename__ = 'invite'

    pass_code = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    num_attending = Column(Integer)
    song_requests = relationship('Song', secondary=song_requests)

class Song(base):
    __tablename__ = 'song'

    id = Column(Integer, primary_key=True)
    track = Column(String)
    artist = Column(String)
    image_url = Column(String)
    requestors = relationship('Invite', secondary=song_requests)

def get_engine():
  config = configparser.ConfigParser(allow_no_value=True)
  config.read('wedding_site_backend/config.ini')

  return create_engine(
      URL(config['database']['database_dialect'], **config['database_url']),
      echo=True)
