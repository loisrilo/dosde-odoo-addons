# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MoneyPot(models.Model):
    _name = "money.pot"
    _order = "id desc"

    name = fields.Char(required=True)
    item_ids = fields.One2many(
        string="Items",
        comodel_name="money.item",
        inverse_name="pot_id",
    )
    user_ids = fields.Many2many(
        string="Users",
        comodel_name="res.users",
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Pot name already exists"),
    ]
