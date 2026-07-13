# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import base64

from odoo.tests.common import HttpCase, tagged


@tagged("-at_install", "post_install")
class TestMusicTrackController(HttpCase):
    def test_download_zip(self):
        artist = self.env["music.artist"].create({"name": "Test Artist"})
        track = self.env["music.track"].create(
            {
                "name": "Test Track",
                "artist_id": artist.id,
                "file": base64.b64encode(b"fake mp3 content"),
            }
        )
        self.authenticate("admin", "admin")
        response = self.url_open(f"/web/music_track/download_zip?ids={track.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Type"), "application/zip")
