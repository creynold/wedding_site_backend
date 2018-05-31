from sqlalchemy import Column, String, ForeignKey, Integer, create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.schema import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker

BaseModel = declarative_base()

song_requests = Table(
    'song_requests', BaseModel.metadata,
    Column('invite_id', String, ForeignKey('invite.pass_code')),
    Column('song_id', Integer, ForeignKey('song.id'))
)

class Invite(BaseModel):
    __tablename__ = 'invite'

    pass_code = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    num_attending = Column(Integer)
    song_requests = relationship('Song', secondary=song_requests)

    @classmethod
    def get(pass_code, session):
        with session.begin():
            invite = session.query(Invite).get(pass_code.lower().strip())
        return invite

    @classmethod
    def get_all(session):
        invites = []
        with session.begin():
          invites = session.query(Invite).all()
        return invites

    def save(self, session):
        with session.begin():
            session.add(self)

class Song(BaseModel):
    __tablename__ = 'song'

    id = Column(Integer, primary_key=True)
    track = Column(String)
    artist = Column(String)
    album = Column(String)
    image_url = Column(String)
    requestors = relationship('Invite', secondary=song_requests)

    @classmethod
    def get_all(session):
        songs = []
        with session.begin():
            songs = session.query(Song).all()
        return songs

    @classmethod
    def find_songs(track, artist, session):
        found_songs = []
        with session.begin():
            found_songs = session.query(Song).filter_by(track=track, artist=artist).all()
        return found_songs

    def save(self, session):
        with session.begin():
            session.add(self)
