# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Library Book"
    _check_company_auto = True

    def _get_registry_number(self):
        last = self.search(
            [("company_id", "=", self.env.company.id)],
            order="registry_number desc",
            limit=1,
        )
        last_number = last and last.registry_number or 0
        return last_number + 1

    name = fields.Char(
        string="Title",
        required=True,
    )
    author_id = fields.Many2one(
        comodel_name="library.author",
        check_company=True,
        required=True,
        ondelete="restrict",
    )
    editorial_id = fields.Many2one(
        comodel_name="library.editorial",
        check_company=True,
        ondelete="restrict",
    )
    collection = fields.Char()
    city = fields.Char()
    year = fields.Integer()
    edition = fields.Char()
    page_total = fields.Integer(
        string="Pages",
    )
    genre_id = fields.Many2one(
        comodel_name="library.genre",
        check_company=True,
        ondelete="restrict",
    )
    registry_number = fields.Integer(
        default=_get_registry_number,
    )
    description = fields.Text()
    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.company,
        index=True,
    )
