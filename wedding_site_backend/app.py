import falcon

from .invite import InviteResource

api = application = falcon.API()

invites = InviteResource()
api.add_route('/invites', invites)
