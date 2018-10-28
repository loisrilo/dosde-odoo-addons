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
    state = fields.Selection(
        selection=[('open', 'Open'),
                   ('closed', 'Closed')],
        default='open',
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Pot name already exists"),
    ]

    @api.multi
    def action_close(self):
        self.write({'state': 'closed'})

    @api.multi
    def action_open(self):
        self.write({'state': 'open'})

    @api.multi
    def action_open_items(self):
        action = self.env.ref('money_pot.money_item_action')
        result = action.read()[0]
        result['domain'] = [('pot_id', '=', self.id)]
        result['context'] = {'search_default_group_by_user': 1}
        return result
