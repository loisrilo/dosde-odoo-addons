# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class MusicArtist(models.Model):
    _name = "music.artist"
    _description = "Artist"
    _order = "name"

    name = fields.Char(required=True)
    track_ids = fields.One2many(
        comodel_name="music.track",
        inverse_name="artist_id",
    )
