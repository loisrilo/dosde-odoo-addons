# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class LibraryAuthor(models.Model):
    _name = "cd.library.author"
    _description = "CD Library Author"
    _order = "name"

    name = fields.Char(required=True)
    disk_ids = fields.One2many(
        comodel_name="cd.library.disk",
        inverse_name="author_id",
    )
    description = fields.Text()
