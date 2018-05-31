import falcon

from .invite import InviteResource
from .songs import SongResource
from .config import Config
from .last_fm import TrackSearch
from .responses import Responses
from .auth_middleware import CheckPassCode

config = Config()
dbmanager = DBManager(config)

api = application = falcon.API(middleware=[CheckPassCode(dbmanager)])

invites = InviteResource(dbmanager)
songs = SongResource(dbmanager)
track_search = TrackSearch(config)
responses = Responses(config, dbmanager)
api.add_route('/invites', invites)
api.add_route('/songs', songs)
api.add_route('/search', track_search)
api.add_route('/responses', responses)
