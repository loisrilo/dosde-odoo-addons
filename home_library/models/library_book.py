# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Library Book"

    def _get_registry_number(self):
        last = self.search([], order="registry_number desc", limit=1)
        last_number = last and last.registry_number or 0
        return last_number + 1

    name = fields.Char(required=True)
    author_id = fields.Many2one(
        comodel_name="library.author",
        required=True,
    )
    editorial_id = fields.Many2one(
        comodel_name="library.editorial",
    )
    collection = fields.Char()
    city = fields.Char()
    year = fields.Integer()
    edition = fields.Char()
    page_total = fields.Integer(
        string="Pages",
    )
    genre_id = fields.Many2one(
        comodel_name="library.genre"
    )
    registry_number = fields.Integer(
        default=_get_registry_number,
    )
    description = fields.Text()
