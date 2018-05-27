import falcon
import json
from .database import Invite, start_session

class CheckPassCode(object):

    def __init__(self, config):
        self.config = config

    def process_request(self, request, response):
        request.session = start_session(self.config)

        if request.path == '/responses':
            return

        if request.method == 'GET':
            pass_code = request.get_param('pass_code')
        else:
            pass_code = request.media.get('pass_code')

        if pass_code is None:
            raise falcon.HTTPUnauthorized('Pass code required')

        invite = request.session.query(Invite).get(pass_code.lower().strip())
        if invite is None:
            raise falcon.HTTPForbidden('Passphrase not recognized!')

        request.invite = invite

    def process_response(self, request, response, resource, req_succeeded):
        if hasattr(response, 'response_json'):
            response.body = json.dumps(response.response_json)
            response.content_type = falcon.MEDIA_JSON
