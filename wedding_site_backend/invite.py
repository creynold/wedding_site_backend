import falcon
import json
from sqlalchemy.orm.session import sessionmaker
from .database import Invite, get_engine

class InviteResource(object):

    def on_get(self, request, response):
        pass_code = request.get_param('pass_code')

        if pass_code is None:
            response.status = falcon.HTTP_400
            return

        engine = get_engine()
        Session = sessionmaker(engine)
        session = Session()

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
