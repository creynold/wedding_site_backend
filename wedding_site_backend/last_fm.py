import falcon
import requests

class LastFm(object):

  _last_fm_url = 'http://ws.audioscrobbler.com/2.0/'
  _format = 'json'
  _limit = '5'

  def __init__(self, config, track=None, artist=None, page=0):
      self.api_key = config.get('last_fm', 'api_key')
      self.track = track
      self.artist = artist
      self.page = page

  def search(self):
      method = 'track.search'
      result = requests.get(self._last_fm_url, {
          'format': self._format,
          'api_key': self.api_key,
          'method': method,
          'track': self.track,
          'artist': self.artist,
          'limit': self._limit,
          'page': self.page
      }).json()['results']

      self.num_results = int(result['opensearch:totalResults'])
      self.items_per_page = int(result['opensearch:itemsPerPage'])
      self.start_index = int(result['opensearch:startIndex'])
      self.tracks = result['trackmatches']['track']

  def get_info(self, artist):
      method = 'track.getInfo'
      result = requests.get(self._last_fm_url, {
          'format': self._format,
          'api_key': self.api_key,
          'method': method,
          'track': self.track,
          'artist': artist
      }).json()

      return {
          'album': result['track']['album']['title'],
          'image_url': result['track']['album']['image'][2]['#text']
      } if 'track' in result and 'album' in result['track'] else None


class TrackSearch(object):

    def __init__(self, config):
        self.config = config

    def _format_track(track, last_fm):
        album_data = last_fm.get_info(track['artist'])
        return {
            'track': track['name'],
            'artist': track['artist'],
            'album': album_data['album'],
            'image_url': album_data['image_url']
        } if album_data is not None else {
            'track': track['name'],
            'artist': track['artist'],
            'image_url': track['image'][2]['#text']
        }

    def on_get(self, request, response):
        track = request.get_param('track')
        if track is None:
            raise falcon.HTTPBadRequest()

        last_fm = LastFm(self.config, track=track, artist=request.get_param('artist'))
        last_fm.search()

        tracks = [TrackSearch._format_track(track, last_fm) for track in last_fm.tracks]

        response.response_json = {'tracks': tracks}
