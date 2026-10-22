# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestLibraryBookTag(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Tag = cls.env["library.book.tag"]
        cls.company_b = cls.env["res.company"].create({"name": "Company B"})
        cls.author = cls.env["library.author"].create(
            {"name": "Tag Author", "company_id": False}
        )

    def test_tag_name_unique_per_company(self):
        self.Tag.create({"name": "Test Tag Novelas"})
        self.Tag.create({"name": "Test Tag Novelas", "company_id": self.company_b.id})
        with mute_logger("odoo.sql_db"), self.assertRaises(IntegrityError):
            self.Tag.create({"name": "Test Tag Novelas"})
            self.env.flush_all()

    def test_book_tags(self):
        tag = self.Tag.create({"name": "Test Tag Recetas"})
        book = self.env["library.book"].create(
            {"name": "Book", "author_id": self.author.id, "tag_ids": [(4, tag.id)]}
        )
        self.assertEqual(book.tag_ids, tag)
        self.assertTrue(1 <= tag.color <= 11)
        other = self.Tag.create(
            {"name": "Test Tag Other", "company_id": self.company_b.id}
        )
        with self.assertRaises(UserError):
            book.tag_ids = [(4, other.id)]
