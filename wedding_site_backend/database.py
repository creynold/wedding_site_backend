from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.schema import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

base = declarative_base()

song_requests = Table(
    'song_requests', base.metadata,
    Column('invite_id', String, ForeignKey('invite.email')),
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
