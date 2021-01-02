# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Librarydisk(models.Model):
    _name = "cd.library.disk"
    _description = "CD Library Disk"

    def _get_registry_number(self):
        last = self.search([], order="registry_number desc", limit=1)
        last_number = last and last.registry_number or 0
        return last_number + 1

    name = fields.Char(
        string="Title",
        required=True,
    )
    author_id = fields.Many2one(
        comodel_name="cd.library.author",
        required=True,
        ondelete="restrict",
    )
    editorial_id = fields.Many2one(
        comodel_name="cd.library.editorial",
        ondelete="restrict",
    )
    city = fields.Char()
    year = fields.Integer()
    genre_id = fields.Many2one(
        comodel_name="cd.library.genre",
        ondelete="restrict",
    )
    registry_number = fields.Integer(
        default=_get_registry_number,
    )
    description = fields.Text()
