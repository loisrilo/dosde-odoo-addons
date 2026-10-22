# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

LANGUAGES = [
    ("gl", "Galician"),
    ("es", "Spanish"),
    ("pt", "Portuguese"),
    ("ca", "Catalan"),
    ("eu", "Basque"),
    ("en", "English"),
    ("fr", "French"),
    ("it", "Italian"),
    ("de", "German"),
    ("la", "Latin"),
    ("other", "Other"),
]


class LibraryBook(models.Model):
    _name = "library.book"
    _inherit = ["mail.thread"]
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
        tracking=True,
    )
    author_id = fields.Many2one(
        comodel_name="library.author",
        check_company=True,
        required=True,
        ondelete="restrict",
        tracking=True,
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
    tag_ids = fields.Many2many(
        comodel_name="library.book.tag",
        string="Tags",
        check_company=True,
    )
    registry_number = fields.Integer(
        default=_get_registry_number,
        tracking=True,
    )
    description = fields.Text()
    language = fields.Selection(selection=LANGUAGES)
    original_title = fields.Char(help="Title of the original work, for translations.")
    original_language = fields.Selection(
        selection=LANGUAGES,
        help="Language of the original work, for translations.",
    )
    udc = fields.Char(
        string="UDC",
        index=True,
        help="Universal Decimal Classification of the book, e.g. 821.134.4-31.",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.company,
        index=True,
        tracking=True,
    )

    _sql_constraints = [
        (
            "registry_number_company_uniq",
            "unique(company_id, registry_number)",
            "Another book of this company already has this registry number. "
            "Choose a different one.",
        ),
    ]
