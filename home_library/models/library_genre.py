# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LibraryGenre(models.Model):
    _name = "library.genre"
    _description = "Library Genre"
    _order = "name"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    description = fields.Text()
    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.company,
        index=True,
    )
