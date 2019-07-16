"""
FIP (web)Radio(s) playlist (previous, current and future tracks).

"""
import json

import requests

BASE_URL = 'https://www.fip.fr/latest/api/graphql?operationName=Now'
VAR_URL = '&variables={"bannerPreset":"600x600-noTransform","stationId":'
TRACK_URL = ',"previousTrackLimit":3}'
EXTENSION_URL = '&extensions={"persistedQuery":{"version":1,"sha256Hash":"'
END_URL = '"}}'

RADIOS_DATA = {
        'fip': {'data_id': '7',
                'stream':
                "https://direct.fipradio.fr/live/fip-midfi.mp3?ID=radiofrance",
                'color': {
                         'red': 226,
                         'green': 0,
                         'blue': 122
                         }
                },
        'fip-electro': {'data_id': '74',
                        'stream':
                        'http://direct.fipradio.fr/live/fip-webradio8.mp3',
                        'color': {
                            'red': 0,
                            'green': 211,
                            'blue': 255
                            }
                        },
        'fip-jazz': {'data_id': '65',
                     'stream':
                     'http://direct.fipradio.fr/live/fip-webradio2.mp3',
                     'color': {
                         'red': 19,
                         'green': 137,
                         'blue': 141
                         }
                     },
        'fip-groove': {'data_id': '66',
                       'stream':
                       'http://direct.fipradio.fr/live/fip-webradio3.mp3',
                       'color': {
                           'red': 134,
                           'green': 100,
                           'blue': 238
                           }
                       },
        'fip-rock': {'data_id': '64',
                     'stream':
                     'http://direct.fipradio.fr/live/fip-webradio1.mp3',
                     'color': {
                         'red': 249,
                         'green': 52,
                         'blue': 70
                         }
                     },
        'fip-monde': {'data_id': '69',
                      'stream':
                      'http://direct.fipradio.fr/live/fip-webradio4.mp3',
                      'color': {
                          'red': 239,
                          'green': 164,
                          'blue': 57
                          }
                      },
        'fip-nouveau': {'data_id': '70',
                        'stream':
                        'http://direct.fipradio.fr/live/fip-webradio5.mp3',
                        'color': {
                            'red': 53,
                            'green': 125,
                            'blue': 237
                            }
                        },
        'fip-reggae': {'data_id': '71',
                       'stream':
                       'http://direct.fipradio.fr/live/fip-webradio6.mp3',
                       'color': {
                           'red': 71,
                           'green': 116,
                           'blue': 66
                           }
                       },
        'fip-metal': {'data_id': '77',
                      'stream':
                      'http://direct.fipradio.fr/live/fip-webradio7.mp3',
                      'color': {
                          'red': 80,
                          'green': 66,
                          'blue': 116
                          }
                      }
                }


class fipplaylistError(Exception):
    """Raise when errors occur while fetching or parsing Fip Radio data"""


class fipplaylistClient():
    """
    Client to fetch and parse data from Meteo-France

    Attributes
    ----------
    station_name : string
        The station name : can be either
                - fip
                - fip-electro
                - fip-rock
                - fip-reggae
                - fip-jazz
                - fip-monde
                - fip-nouveau
                - fip-metal
                - fip-groove
    update : boolean
        if True, the data is fetch immediately after creation

    external_data : string
        string containing the json answer from fip.fr website (debug purpose)

    persistedQueryID : string
        string containing the persistedQueryID used by the graphql request.

    Methods
    -------
    update()
        return the playlist + infos

    """

    PERSISTEDQUERY_HASH = \
        '8a931c7d177ff69709a79f4c213bd2403f0c11836c560bc22da55628d8100df8'

    def __init__(self,
                 station_name,
                 update=False,
                 external_data=False,
                 persistedQueryID=PERSISTEDQUERY_HASH):
        """Initialize the client object"""
        if (station_name is None or
                station_name not in RADIOS_DATA.keys()):
            raise fipplaylistError(
                "Error: name %s not recognized",
                station_name
                )

        self._station_name = station_name
        self._station_id = RADIOS_DATA[station_name]['data_id']
        self._stream_url = RADIOS_DATA[station_name]['stream']
        self._station_color = RADIOS_DATA[station_name]['color']
        self._metadata_url = BASE_URL + VAR_URL + self._station_id +\
            TRACK_URL + EXTENSION_URL + persistedQueryID + END_URL
        self._next_refresh = False
        self._current_broadcast = False
        self._previous_tracks = False
        self._current_track = False
        self._next_tracks = False
        self._jsondata = False

        if (external_data is not False):
            self._jsondata = json.loads(external_data)

        if (update is not False):
            self.update()

    def update(self):
        """Go fetch new data and format it"""

        if (self._jsondata is False):
            self._fetch_metadata()
        return self._format_data()

    async def _fetch_metadata(self):
        """Get playlist content"""
        try:
            self._jsondata = \
                requests.get(self._metadata_url, timeout=10).json()
        except Exception as err:
            raise fipplaylistError(err)

    def _format_data(self):
        """Format data return by FIP radio """

        try:
            now = (self._jsondata)['data']['now']
            self._next_refresh = now['next_refresh']

            if 'song' in now and now['song'] is not None:
                self._current_track = {
                    'title': now['song']['title'],
                    'artist': now['song']['interpreters'][0],
                    'cover': now['song']['cover'],
                    'start_time': now['playing_item']['start_time'],
                    'end_time': now['playing_item']['end_time']
                }
            else:
                self._current_track = {
                    'title': now['playing_item']['title'],
                    'artist': now['playing_item']['subtitle'],
                    'cover': now['playing_item']['cover'],
                    'start_time': now['playing_item']['start_time'],
                    'end_time': now['playing_item']['end_time']
                    }

            previousTracks = self._jsondata['data']['previousTracks']['edges']
            for i in range(0, len(previousTracks)):
                if (i == 0):
                    self._previous_tracks = []
                track = previousTracks[i]['node']
                if (i == len(previousTracks)-1):
                    end = now['playing_item']['start_time']
                else:
                    end = previousTracks[i+1]['node']['start_time']
                self._previous_tracks.append({
                    'title': track['subtitle'],
                    'artist': track['title'],
                    'cover': track['cover'],
                    'start_time': track['start_time'],
                    'end_time': end
                })

            nextTracks = self._jsondata['data']['nextTracks']

            for i in range(0, len(nextTracks)):
                if (i == 0):
                    self._next_tracks = []

                if (len(nextTracks) == 1):
                    track = nextTracks[i]
                else:
                    track = nextTracks[i]['node']

                self._next_tracks.append({
                    'title': track['subtitle'],
                    'artist': track['title'],
                    'cover': track['cover'],
                    'start_time': track['start_time'],
                    'end_time': None
                })

            return {'current_track': self._current_track,
                    'broadcast': self._current_broadcast,
                    'previous_tracks': self._previous_tracks,
                    'next_tracks': self._next_tracks,
                    'stream': self._stream_url,
                    'color': self._station_color,
                    'attribution': "Open API Radio France - FIP Radio"}

        except Exception as err:
            raise fipplaylistError(err)
