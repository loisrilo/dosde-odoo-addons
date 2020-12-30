# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class LibraryAuthor(models.Model):
    _name = "library.author"
    _description = "Library Author"

    name = fields.Char(required=True)
    book_ids = fields.One2many(
        comodel_name="library.book",
        inverse_name="author_id",
    )
    description = fields.Text()
