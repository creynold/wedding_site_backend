import falcon
import json
from .database import Invite, Song, start_session

class SongResource(object):

    def __init__(self, config):
        self.config = config

    # track, artist, image_url, requestors
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
