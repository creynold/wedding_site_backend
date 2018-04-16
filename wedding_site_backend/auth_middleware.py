import falcon
import json
from .database import Invite, start_session

class CheckPassCode(object):

    def __init__(self, config):
        self.config = config

    def process_request(self, request, response):
        if request.method == 'GET':
            pass_code = request.get_param('pass_code')
        else:
            pass_code = request.media.get('pass_code')

        if pass_code is None:
            raise falcon.HTTPUnauthorized('Pass code required')

        session = start_session(self.config)

        invite = session.query(Invite).get(pass_code)
        if invite is None:
            raise falcon.HTTPForbidden()

        request.invite = invite
        request.session = session

    def process_response(self, request, response, resource, req_succeeded):
        response.body = json.dumps(response.response_json)
        response.content_type = falcon.MEDIA_JSON
