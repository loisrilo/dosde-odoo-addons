# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestLibraryBook(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = cls.env["library.author"].create({"name": "Test Author"})
        cls.editorial = cls.env["library.editorial"].create({"name": "Test Editorial"})
        cls.genre = cls.env["library.genre"].create({"name": "Test Genre"})

    def test_create_book(self):
        book = self.env["library.book"].create(
            {
                "name": "Test Book",
                "author_id": self.author.id,
                "editorial_id": self.editorial.id,
                "genre_id": self.genre.id,
            }
        )
        self.assertEqual(book.author_id, self.author)
        self.assertIn(book, self.author.book_ids)

    def test_registry_number_auto_increment(self):
        book_1 = self.env["library.book"].create(
            {"name": "Book 1", "author_id": self.author.id}
        )
        book_2 = self.env["library.book"].create(
            {"name": "Book 2", "author_id": self.author.id}
        )
        self.assertEqual(book_2.registry_number, book_1.registry_number + 1)

    def test_registry_number_tracking(self):
        book = self.env["library.book"].create(
            {"name": "Tracked Book", "author_id": self.author.id}
        )
        old_number = book.registry_number
        self.env.flush_all()
        self.env.cr.precommit.run()
        book.registry_number = old_number + 100
        self.env.flush_all()
        self.env.cr.precommit.run()
        tracking = book.message_ids.tracking_value_ids.filtered(
            lambda t: t.field_id.name == "registry_number"
        )
        self.assertEqual(len(tracking), 1)
        self.assertEqual(tracking.old_value_integer, old_number)
        self.assertEqual(tracking.new_value_integer, old_number + 100)

    def test_settings_app(self):
        arch = self.env["res.config.settings"].get_views([(False, "form")])["views"][
            "form"
        ]["arch"]
        self.assertIn('name="home_library"', arch)
        self.assertIn('name="home_library_catalog"', arch)
