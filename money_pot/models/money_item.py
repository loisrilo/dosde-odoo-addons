# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MoneyItem(models.Model):
    _name = "money.item"
    _order = "id desc"
    _rec_name = "user_id"

    @api.multi
    def _get_pot_id(self):
        return self.env['money.pot'].search(
            [('user_ids', '=', self.env.uid), ('state', '=', 'open')],
            order="id desc", limit=1)

    pot_id = fields.Many2one(
        comodel_name="money.pot",
        required=True,
        default=_get_pot_id,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        default=lambda self: self.env.user,
        required=True,
    )
    date = fields.Date(
        required=True,
        default=fields.Date.today,
    )
    amount = fields.Float()
    description = fields.Char()

    @api.constrains('pot_id')
    def _check_pot_open(self):
        for rec in self:
            if rec.pot_id.state == 'closed':
                raise ValidationError(_('Pot is closed.'))
