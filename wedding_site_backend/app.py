import falcon

from .invite import InviteResource
from .songs import SongResource
from .config import Config
from .last_fm import TrackSearch

api = application = falcon.API()
config = Config()

invites = InviteResource(config)
songs = SongResource(config)
track_search = TrackSearch(config)
api.add_route('/invites', invites)
api.add_route('/songs', songs)
api.add_route('/search', track_search)
