# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class WashTurn(models.Model):
    _name = "wash.turn"
    _order = "date desc"
    _rec_name = 'date'

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        default=lambda self: self.env.user,
        required=True,
    )
    date = fields.Date(required=True)
    notes = fields.Html()
    past = fields.Boolean(compute='_compute_past')

    _sql_constraints = [
        ('date_uniq', 'unique (date)', "Date unavailable"),
    ]

    @api.constrains("date")
    def _check_date(self):
        for rec in self:
            if rec.date < fields.Date.today():
                raise ValidationError(_(
                    "You cannot travel to the past, do you?"))

    @api.multi
    def _compute_past(self):
        today = fields.Date.today()
        for rec in self:
            rec.past = rec.date < today

    @api.multi
    def write(self, vals):
        user = self.env.user
        if (not user.has_group('washing_machine.group_washing_machine_manager')
                and (self.mapped('user_id') != user or
                     any(self.mapped('past')))):
            raise ValidationError(_(
                "You are not allowed to write other user's turns or "
                "past turns."))
        return super().write(vals)
