# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Home Library",
    "summary": "Manage a simple registry of books.",
    "version": "14.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://github.com/loisrilo/",
    "author": "Lois Rilo",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        "security/home_library_security.xml",
        "security/ir.model.access.csv",
        "views/library_book_view.xml",
        "views/library_author_view.xml",
        "views/library_editorial_view.xml",
        "views/library_genre_view.xml",
    ],
}
