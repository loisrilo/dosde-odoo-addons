# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo.exceptions import UserError
from odoo.tests import new_test_user, tagged
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestLibraryMultiCompany(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_a = cls.env.company
        cls.company_b = cls.env["res.company"].create({"name": "Company B"})
        cls.user_a = new_test_user(
            cls.env,
            login="library_user_a",
            groups="home_library.group_home_library_user",
            company_id=cls.company_a.id,
            company_ids=[(6, 0, cls.company_a.ids)],
        )
        cls.author_a = cls.env["library.author"].create({"name": "Author A"})
        cls.author_b = (
            cls.env["library.author"]
            .with_company(cls.company_b)
            .create({"name": "Author B"})
        )
        cls.author_shared = cls.env["library.author"].create(
            {"name": "Shared Author", "company_id": False}
        )

    def test_company_default(self):
        self.assertEqual(self.author_a.company_id, self.company_a)
        self.assertEqual(self.author_b.company_id, self.company_b)
        book = self.env["library.book"].create(
            {"name": "Book A", "author_id": self.author_a.id}
        )
        self.assertEqual(book.company_id, self.company_a)

    def test_record_rule(self):
        authors = self.env["library.author"].with_user(self.user_a).search([])
        self.assertIn(self.author_a, authors)
        self.assertIn(self.author_shared, authors)
        self.assertNotIn(self.author_b, authors)

    def test_check_company(self):
        with self.assertRaises(UserError):
            self.env["library.book"].create(
                {
                    "name": "Mixed Book",
                    "author_id": self.author_b.id,
                    "company_id": self.company_a.id,
                }
            )
        book = self.env["library.book"].create(
            {"name": "Shared Author Book", "author_id": self.author_shared.id}
        )
        self.assertEqual(book.author_id, self.author_shared)

    def test_registry_number_per_company(self):
        book_a = self.env["library.book"].create(
            {"name": "Book A", "author_id": self.author_a.id}
        )
        book_b = (
            self.env["library.book"]
            .with_company(self.company_b)
            .create({"name": "Book B", "author_id": self.author_b.id})
        )
        self.assertEqual(book_b.registry_number, 1)
        self.assertGreaterEqual(book_a.registry_number, 1)

    def test_registry_number_unique_per_company(self):
        book_a = self.env["library.book"].create(
            {"name": "Book A", "author_id": self.author_a.id}
        )
        with mute_logger("odoo.sql_db"), self.assertRaises(IntegrityError):
            self.env["library.book"].create(
                {
                    "name": "Book A bis",
                    "author_id": self.author_a.id,
                    "registry_number": book_a.registry_number,
                }
            )
            self.env.flush_all()

    def test_registry_number_kept_or_rejected_on_company_change(self):
        book_a = self.env["library.book"].create(
            {"name": "Book A", "author_id": self.author_shared.id}
        )
        book_b = (
            self.env["library.book"]
            .with_company(self.company_b)
            .create({"name": "Book B", "author_id": self.author_shared.id})
        )
        self.assertEqual(book_b.registry_number, 1)
        book_a.registry_number = 1000
        book_a.company_id = self.company_b
        self.env.flush_all()
        self.assertEqual(book_a.registry_number, 1000)
        with mute_logger("odoo.sql_db"), self.assertRaises(IntegrityError):
            book_a.registry_number = book_b.registry_number
            self.env.flush_all()
