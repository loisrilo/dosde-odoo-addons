# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class WashTurn(models.Model):
    _name = "wash.turn"
    _order = "date desc"

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

    @api.constrains("date")
    def _check_date(self):
        for rec in self:
            if rec.date < fields.Date.today():
                raise ValidationError(_(
                    "You cannot travel to the past, do you?"))
