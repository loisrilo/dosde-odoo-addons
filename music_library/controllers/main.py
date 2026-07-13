# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import _, http
from odoo.http import request


class MusicLibraryController(http.Controller):
    @http.route("/web/music_track/download_zip", type="http", auth="user")
    def download_zip(self, ids=None):
        ids = [] if not ids else ids
        if len(ids) == 0:
            return
        list_ids = map(int, ids.split(","))
        out_file = request.env["music.track"].browse(list_ids)._create_temp_zip()
        stream = http.Stream(
            type="data",
            data=out_file.getvalue(),
            mimetype="application/zip",
            as_attachment=True,
            download_name=_("music.zip"),
        )
        return stream.get_response()
