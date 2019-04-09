# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Housekeeping",
    "summary": "Manage Housekeeping tasks.",
    "version": "12.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://github.com/loisrilo/",
    "author": "Lois Rilo",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "mail",
    ],
    "data": [
        "security/housekeeping_security.xml",
        "security/ir.model.access.csv",
        "data/housekeeping_data.xml",
        "views/housekeeping_view.xml",
        "views/house_task_view.xml",
    ],
}
