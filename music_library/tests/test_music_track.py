# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestMusicTrack(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.artist = cls.env["music.artist"].create({"name": "Test Artist"})

    def test_compute_filename(self):
        track = self.env["music.track"].create(
            {"name": "Test Track", "artist_id": self.artist.id}
        )
        self.assertEqual(track.filename, "Test Artist - Test Track.mp3")

    def test_action_music_zip_download(self):
        track = self.env["music.track"].create(
            {"name": "Test Track", "artist_id": self.artist.id}
        )
        action = track.action_music_zip_download()
        self.assertEqual(action["type"], "ir.actions.act_url")
        self.assertIn(str(track.id), action["url"])
