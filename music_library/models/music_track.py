# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


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
            rec.filename = "%s - %s" % (rec.artist_id.name, rec.name)
