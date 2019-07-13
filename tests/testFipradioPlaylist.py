import unittest
from fipradioPlaylist import client


class TestPlaylistData(unittest.TestCase):

    def testCurrentTrackt(self):
        clientPlaylist = client.fipplaylistClient(
            station_name='fip',
            external_data='{"data":{"now":{"__typename":"Now","playing_item":{"__typename":"TimelineItem","title":"CALIBRO 35","subtitle":"AMBIENTI","cover":"https://e-cdns-images.dzcdn.net/images/cover/c83da7d56fa06f26e3acd0fe48f20f12/1000x1000-000000-80-0-0.jpg","start_time":1562589820,"end_time":1562590005},"program":null,"song":{"__typename":"SongOnAir","cover":"https://e-cdns-images.dzcdn.net/images/cover/c83da7d56fa06f26e3acd0fe48f20f12/1000x1000-000000-80-0-0.jpg","title":"AMBIENTI","interpreters":["CALIBRO 35"],"musical_kind":"SOUL/FUNK","label":"RECORD KICKS","album":"Decade","external_links":{"youtube":{"id":"u-iLKLjS3ec","link":"https://www.youtube.com/watch?v=u-iLKLjS3ec","image":"https://i.ytimg.com/vi/u-iLKLjS3ec/hqdefault.jpg","__typename":"ExternalLink"},"deezer":{"id":"448048922","link":"https://www.deezer.com/track/448048922","image":"https://e-cdns-images.dzcdn.net/images/cover/c83da7d56fa06f26e3acd0fe48f20f12/1000x1000-000000-80-0-0.jpg","__typename":"ExternalLink"},"itunes":{"id":"1333170942","link":"https://music.apple.com/fr/album/ambienti/1333170241?i=1333170942&uo=4","image":"https://is4-ssl.mzstatic.com/image/thumb/Music118/v4/69/e9/d3/69e9d321-9faa-7b8d-5862-e93c193eb300/source/100x100bb.jpg","__typename":"ExternalLink"},"spotify":{"id":"06reouC1XnZSFghqCEFFpE","link":"https://open.spotify.com/track/06reouC1XnZSFghqCEFFpE","image":"https://i.scdn.co/image/bfed0721860b1329f5e6f324488195d69d8868e9","__typename":"ExternalLink"},"__typename":"ExternalLinks"}},"server_time":1562589828,"next_refresh":1562590006,"mode":"song"},"previousTracks":{"__typename":"HistoryCursor","edges":[{"__typename":"TimeLineItemEdge","node":{"__typename":"TimelineItem","title":"YOANN MINKOFF","subtitle":"DEVIL IN A FANCY DRESS","start_time":1562589553,"cover":"https://is4-ssl.mzstatic.com/image/thumb/Music118/v4/1d/de/c1/1ddec170-5451-49e2-cc4d-f79b29ffe944/source/400x400bb.jpg"}},{"__typename":"TimeLineItemEdge","node":{"__typename":"TimelineItem","title":"NICOLAS MICHAUX","subtitle":"LES ILES DESERTES","start_time":1562589410,"cover":"https://e-cdns-images.dzcdn.net/images/cover/27c22a654aa68d5683bca3a8c8ac5b1b/1000x1000-000000-80-0-0.jpg"}},{"__typename":"TimeLineItemEdge","node":{"__typename":"TimelineItem","title":"FRED WILLIAMS & THE JEWELS BAND","subtitle":"TELL HER","start_time":1562589273,"cover":"https://e-cdns-images.dzcdn.net/images/cover/52e91f365e103e3e7ec956c8ab1aa3f1/1000x1000-000000-80-0-0.jpg"}}]},"nextTracks":[{"__typename":"TimelineItem","title":"ETTA JAMES","subtitle":"I GOT YOU BABE","start_time":1562590007,"cover":"https://e-cdns-images.dzcdn.net/images/cover/3ae04f8bace6154b552d67ad9e019730/1000x1000-000000-80-0-0.jpg"}]}}')
        dataPlaylist = clientPlaylist.update()
        print(dataPlaylist)
        assert dataPlaylist['current_track'] is not None
        assert len(dataPlaylist['previous_tracks']) == 3
        assert len(dataPlaylist['next_tracks']) == 1
        return(True)

    def testFipStreamingURL(self):
        clientPlaylist = client.fipplaylistClient(
            station_name='fip',
            external_data='{"data":{"now":{"__typename":"Now","playing_item":{"__typename":"TimelineItem","title":null,"subtitle":null,"cover":null,"start_time":0,"end_time":0},"program":null,"song":null,"server_time":1562950804,"next_refresh":1562950814,"mode":"program"},"previousTracks":{"__typename":"HistoryCursor","edges":[{"__typename":"TimeLineItemEdge","node":{"__typename":"TimelineItem","title":"Paris Combo","subtitle":"Je te vois partout (Taggy Matcher rocksteady remix)","start_time":1562950580,"cover":"https://cdns-images.dzcdn.net/images/cover/79246253c9e5c572b8e937ada6f901ee/1000x1000-000000-80-0-0.jpg"}},{"__typename":"TimeLineItemEdge","node":{"__typename":"TimelineItem","title":"Angelique Kidjo","subtitle":"Sahara","start_time":1562950310,"cover":"https://e-cdns-images.dzcdn.net/images/cover/0f71dcaf1137bddf33708f7bd1dbec2e/1000x1000-000000-80-0-0.jpg"}},{"__typename":"TimeLineItemEdge","node":{"__typename":"TimelineItem","title":"The Knack","subtitle":"My sharona","start_time":1562949905,"cover":"https://e-cdns-images.dzcdn.net/images/cover/14c4093d20e4147cb1b07d001239eba5/1000x1000-000000-80-0-0.jpg"}}]},"nextTracks":[{"__typename":"TimelineItem","title":"Luca Aquino, Danilo Rea, Natalino Marchetti, Fabio Giachino, Rino De Patre","subtitle":"Storia d’amore","start_time":1562950827,"cover":"https://e-cdns-images.dzcdn.net/images/cover/a5f64f6c91565341b4ece7f672ff5897/1000x1000-000000-80-0-0.jpg"}]}}')
        dataPlaylist = clientPlaylist.update()
        print(dataPlaylist)
        assert dataPlaylist['current_track'] is None
        return(False)

    if __name__ == "__main__":
        unittest.main()
