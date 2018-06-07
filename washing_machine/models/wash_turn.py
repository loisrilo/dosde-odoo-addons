# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WashTurn(models.Model):
    _name = "wash.turn"

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        default=lambda self: self.env.user,
        required=True,
    )
    date = fields.Date(required=True)
    notes = fields.Html()

    _sql_constraints = [
        ('date_uniq', 'unique (date)', "Date unavailable"),
    ]
