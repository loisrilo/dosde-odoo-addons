# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "CD Library",
    "summary": "Manage a simple registry of music disks.",
    "version": "13.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://github.com/loisrilo/",
    "author": "Lois Rilo",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        "security/cd_library_security.xml",
        "security/ir.model.access.csv",
        "views/cd_library_disk_view.xml",
        "views/cd_library_author_view.xml",
        "views/cd_library_editorial_view.xml",
        "views/cd_library_genre_view.xml",
    ],
}
