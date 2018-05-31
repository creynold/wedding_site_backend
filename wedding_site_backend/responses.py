import falcon
from .database import Invite, Song

class Responses(object):

    def __init__(self, config, dbmanager):
        self.config = config
        self.dbmanager = dbmanager

    def on_get(self, request, response):
        if request.get_param('password') != self.config.get('misc', 'responses_password'):
            raise falcon.HTTPForbidden()

        invites = Invite.get_all(self.dbmanager.session)

        response.response_json = {
            'rsvps': [self.__convert_invite(invite)
                      for invite in invites
                      if invite.first_name],
        }

        songs = Song.get_all(self.dbmanager.session)
        response.response_json['songs'] = [self.__convert_song(song)
                                           for song in songs
                                           if len(song.requestors) > 0]

    def __convert_invite(self, invite):
        return {
            'first_name': invite.first_name,
            'last_name': invite.last_name,
            'email': invite.email,
            'num_attending': invite.num_attending,
            'num_song_requests': len(invite.song_requests)
        }

    def __convert_song(self, song):
        return {
            'track': song.track,
            'artist': song.artist,
            'album': song.album,
            'requested_by': [requestor.first_name + ' ' + requestor.last_name
                             for requestor in song.requestors]
        }
