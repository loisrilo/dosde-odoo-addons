# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class LibraryGenre(models.Model):
    _name = "music.genre"
    _description = "Genre"
    _order = "name"

    name = fields.Char(required=True)
