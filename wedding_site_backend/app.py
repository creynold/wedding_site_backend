import falcon

from .invite import Invite

api = application = falcon.API()

invites = Invite()
api.add_route('/invites', invites)
