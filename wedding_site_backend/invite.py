import falcon
import json

class Invite(object):

    def on_get(self, request, response):
        test = {'message': 'hello world'}
        response.body = json.dumps(test)
        response.content_type = falcon.MEDIA_JSON
