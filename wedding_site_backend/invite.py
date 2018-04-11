import falcon
import json
from .database import Invite, start_session

class InviteResource(object):

    def __init__(self, config):
        self.config = config

    def on_get(self, request, response):
        pass_code = request.get_param('pass_code')

        if pass_code is None:
            response.status = falcon.HTTP_400
            return

        session = start_session(self.config)

        invite = session.query(Invite).get(pass_code)
        if invite is None:
            response.status = falcon.HTTP_404
            return

        response_json = {
            'first_name': invite.first_name,
            'last_name': invite.last_name,
            'email': invite.email,
            'num_attending': invite.num_attending,
            'num_song_requests': len(invite.song_requests)
        }

        response.body = json.dumps(response_json)
        response.content_type = falcon.MEDIA_JSON

    def on_put(self, request, response):
        request_json = request.media
        pass_code = request_json.get('pass_code')
        if pass_code is None:
            response.status = falcon.HTTP_400
            return

        session = start_session(self.config)

        invite = session.query(Invite).get(pass_code)
        if invite is None:
            response.status = falcon.HTTP_404
            return

        if 'first_name' in request_json:
            invite.first_name = request_json['first_name']

        session.commit()

        response_json = {
            'first_name': invite.first_name,
            'last_name': invite.last_name,
            'email': invite.email,
            'num_attending': invite.num_attending,
            'num_song_requests': len(invite.song_requests)
        }

        response.body = json.dumps(response_json)
        response.content_type = falcon.MEDIA_JSON
