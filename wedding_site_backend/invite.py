import falcon
from .resources import BaseResource

class InviteResource(BaseResource):

    def on_get(self, request, response):
        invite = request.invite

        response.response_json = {
            'first_name': invite.first_name,
            'last_name': invite.last_name,
            'email': invite.email,
            'num_attending': invite.num_attending,
            'num_song_requests': len(invite.song_requests)
        }

    def on_put(self, request, response):
        invite = request.invite
        request_json = request.media

        first_name = request_json.get('first_name')
        last_name = request_json.get('last_name')
        email = request_json.get('email')
        try:
            num_attending = int(request_json.get('num_attending'))
        except:
            num_attending = None

        if first_name is None or last_name is None or email is None:
            raise falcon.HTTPBadRequest()

        invite.first_name = first_name
        invite.last_name = last_name
        invite.email = email
        invite.num_attending = num_attending

        invite.save(self.db.session)

        response.response_json = {
            'first_name': invite.first_name,
            'last_name': invite.last_name,
            'email': invite.email,
            'num_attending': invite.num_attending,
            'num_song_requests': len(invite.song_requests)
        }
