import falcon
from .database import Song

class SongResource(object):

    def on_get(self, request, response):
        invite = request.invite

        response.response_json = {
            'num_song_requests': len(invite.song_requests),
            'tracks': [{
                'track': song.track,
                'artist': song.artist,
                'album': song.album,
                'image_url': song.image_url,
                'song_id': song.id
            } for song in invite.song_requests]
        }

    def on_post(self, request, response):
        request_json = request.media

        invite = request.invite
        session = request.session

        if len(invite.song_requests) >= 5:
            raise falcon.HTTPForbidden('Too many songs added')

        track = request_json.get('track')
        artist = request_json.get('artist')
        image_url = request_json.get('image_url')
        album = request_json.get('album')

        if track is None or artist is None or image_url is None:
            raise falcon.HTTPBadRequest('Missing parameters')

        existing_songs = session.query(Song).filter_by(track=track, artist=artist).all()
        if len(existing_songs) > 0:
            song = existing_songs[0]
            if invite not in song.requestors:
                song.requestors.append(invite)
        else:
            song = Song(track=track, artist=artist, album=album, image_url=image_url)
            song.requestors.append(invite)

            session.add(song)

        session.commit()

        response.response_json = {
            'track': song.track,
            'artist': song.artist,
            'album': song.album,
            'image_url': song.image_url,
            'song_id': song.id
        }

    def on_delete(self, request, response):
        invite = request.invite
        session = request.session
        song_id = request.media.get('song_id')

        response.response_json = {}
        for song in invite.song_requests[:]:
            if song.id == song_id:
                invite.song_requests.remove(song)
                response.response_json = {
                  'track': song.track,
                  'artist': song.artist,
                  'album': song.album,
                  'image_url': song.image_url,
                  'song_id': song.id
                }
                session.commit()
                return

        raise falcon.HTTPNotFound()
