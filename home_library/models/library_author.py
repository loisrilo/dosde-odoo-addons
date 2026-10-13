# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LibraryAuthor(models.Model):
    _name = "library.author"
    _description = "Library Author"
    _order = "name"

    name = fields.Char(required=True)
    book_ids = fields.One2many(
        comodel_name="library.book",
        inverse_name="author_id",
    )
    description = fields.Text()
    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.company,
        index=True,
    )
