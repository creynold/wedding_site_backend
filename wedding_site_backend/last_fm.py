import falcon
import json
import requests
from .database import Invite, start_session

class LastFm(object):

  _last_fm_url = 'http://ws.audioscrobbler.com/2.0/'
  _format = 'json'
  _limit = '5'

  def __init__(self, config, method='track.search', track=None, artist=None, page=0):
      self.api_key = config.get('last_fm', 'api_key')
      self.method = method
      self.track = track
      self.artist = artist
      self.page = page

  def search(self):
      result = requests.get(self._last_fm_url, {
          'format': self._format,
          'api_key': self.api_key,
          'method': self.method,
          'track': self.track,
          'artist': self.artist,
          'limit': self._limit,
          'page': self.page
      }).json()['results']

      self.num_results = int(result['opensearch:totalResults'])
      self.items_per_page = int(result['opensearch:itemsPerPage'])
      self.start_index = int(result['opensearch:startIndex'])
      self.tracks = result['trackmatches']['track']

class TrackSearch(object):

    def __init__(self, config):
        self.config = config

    def _format_track(track):
        return {
            'track': track['name'],
            'artist': track['artist'],
            'image_url': track['image'][2]['#text']
        }

    def on_get(self, request, response):
        pass_code = request.get_param('pass_code')

        if pass_code is None:
            response.status = falcon.HTTP_400
            return

        session = start_session(self.config)

        invite = session.query(Invite).get(pass_code)
        if invite is None:
            response.status = falcon.HTTP_403
            return

        track = request.get_param('track')
        if track is None:
            response.status = falcon.HTTP_400
            return

        last_fm = LastFm(self.config, track=track, artist=request.get_param('artist'))
        last_fm.search()

        tracks = [TrackSearch._format_track(track) for track in last_fm.tracks]

        response.body = json.dumps({'tracks': tracks})
        response.content_type = falcon.MEDIA_JSON
