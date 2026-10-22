# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from random import randint

from odoo import fields, models


class LibraryBookTag(models.Model):
    _name = "library.book.tag"
    _description = "Library Book Tag"
    _order = "name"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True)
    color = fields.Integer(default=_default_color)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.company,
        index=True,
    )

    _sql_constraints = [
        (
            "name_company_uniq",
            "unique(name, company_id)",
            "A tag with this name already exists in this company.",
        ),
    ]
