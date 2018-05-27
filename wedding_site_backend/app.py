import falcon

from .invite import InviteResource
from .songs import SongResource
from .config import Config
from .last_fm import TrackSearch
from .responses import Responses
from .auth_middleware import CheckPassCode

config = Config()
api = application = falcon.API(middleware=[CheckPassCode(config)])

invites = InviteResource()
songs = SongResource()
track_search = TrackSearch(config)
responses = Responses(config)
api.add_route('/invites', invites)
api.add_route('/songs', songs)
api.add_route('/search', track_search)
api.add_route('/responses', responses)
