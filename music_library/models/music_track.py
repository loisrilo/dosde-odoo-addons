# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _

import zipfile
from io import BytesIO


class MusicTrack(models.Model):
    _name = "music.track"
    _description = "Music Track"

    name = fields.Char(
        string="Title",
        required=True,
    )
    artist_id = fields.Many2one(
        comodel_name="music.artist",
        required=True,
        ondelete="restrict",
    )
    album_id = fields.Many2one(
        comodel_name="music.album",
        ondelete="restrict",
    )
    year = fields.Integer()
    genre_id = fields.Many2one(
        comodel_name="music.genre",
        ondelete="restrict",
    )
    file = fields.Binary(attachment=True, copy=False)
    filename = fields.Char(
        compute="_compute_filename",
        readonly=True, store=True, size=256)

    @api.depends("name", "artist_id")
    def _compute_filename(self):
        for rec in self:
            if not rec.name or not rec.artist_id:
                continue
            rec.filename = "%s - %s.mp3" % (rec.artist_id.name, rec.name)

    def action_music_zip_download(self):
        ids = ",".join(map(str, self.ids))
        return {
            "type": "ir.actions.act_url",
            "url": "/web/music_track/download_zip?ids=%s" % (ids),
            "target": "self",
        }

    def _create_temp_zip(self):
        zip_buffer = BytesIO()
        domain = [
            ("res_model", "=", self._name),
            ("res_field", "=", "file"),
            ("res_id", "in", self.ids),
        ]
        attachments = self.env["ir.attachment"].sudo().search(domain)

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for rec in self:
                attachment = attachments.filtered(lambda a: a.res_id == rec.id)
                zip_file.write(
                    attachment._full_path(attachment.store_fname), rec.filename
                )
            zip_buffer.seek(0)
            zip_file.close()
        return zip_buffer
