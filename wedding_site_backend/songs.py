import falcon
import json
from .database import Invite, Song, start_session

class SongResource(object):

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
            'num_song_requests': len(invite.song_requests),
            'tracks': [{
                'track': song.track,
                'artist': song.artist,
                'image_url': song.image_url,
                'song_id': song.id
            } for song in invite.song_requests]
        }

        response.body = json.dumps(response_json)
        response.content_type = falcon.MEDIA_JSON

    def on_post(self, request, response):
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

        if len(invite.song_requests) >= 5:
            response.status = falcon.HTTP_403
            response.body = json.dumps({'message': 'Too many songs added'})
            return

        track = request_json.get('track')
        artist = request_json.get('artist')
        image_url = request_json.get('image_url')

        if track is None or artist is None or image_url is None:
            response.status = falcon.HTTP_400
            response.body = json.dumps({'message': 'missing parameters'})
            return

        existing_songs = session.query(Song).filter_by(track=track, artist=artist).all()
        if len(existing_songs) > 0:
            song = existing_songs[0]
            if invite not in song.requestors:
                song.requestors.append(invite)
        else:
            song = Song(track=track, artist=artist, image_url=image_url)
            song.requestors.append(invite)

            session.add(song)

        session.commit()

        response.body = json.dumps({
            'track': song.track,
            'artist': song.artist,
            'image_url': song.image_url,
            'song_id': song.id
        })
        response.content_type = falcon.MEDIA_JSON

    def on_delete(self, request, response):
        request_json = request.media
        pass_code = request_json.get('pass_code')
        song_id = request_json.get('song_id')
        if pass_code is None or song_id is None:
            response.status = falcon.HTTP_400
            return

        session = start_session(self.config)

        invite = session.query(Invite).get(pass_code)
        if invite is None:
            response.status = falcon.HTTP_404
            return

        response_json = {}
        for song in invite.song_requests[:]:
            if song.id == song_id:
                invite.song_requests.remove(song)
                response_json = {
                  'track': song.track,
                  'artist': song.artist,
                  'image_url': song.image_url,
                  'song_id': song.id
                }

        session.commit()

        response.body = json.dumps(response_json)
        response.content_type = falcon.MEDIA_JSON
