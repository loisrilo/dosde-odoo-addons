# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class MusicAlbum(models.Model):
    _name = "music.album"
    _description = "Album"
    _order = "name"

    name = fields.Char(required=True)
    artist_ids = fields.Many2many(
        comodel_name="music.artist",
        compute="_compute_artist_ids"
    )
    track_ids = fields.One2many(
        comodel_name="music.track",
        inverse_name="album_id",
    )

    def _compute_artist_ids(self):
        for rec in self:
            rec.artist_ids = rec.track_ids.mapped("artist_id")
