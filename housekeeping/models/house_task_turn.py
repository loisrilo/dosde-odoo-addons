# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HouseTaskTurn(models.Model):
    _name = "house.task.turn"
    _description = "Task Turn"
    _inherit = 'mail.thread'
    _order = "id desc"

    name = fields.Char(default="/")
    house_task_id = fields.Many2one(
        string="Task",
        comodel_name="house.task",
        required=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Assigned to",
        default=lambda self: self.env.user,
        required=True,
        tracking=True,
    )
    state = fields.Selection(
        selection=[('pending', 'Pending'),
                   ('done', 'Done'),
                   ('cancel', 'Cancel')],
        default='pending',
        tracking=True,
    )
    date_due = fields.Date(
        string="Deadline",
        required=True,
        tracking=True,
    )
    date_done = fields.Date(
        string="Done Date",
    )
    notes = fields.Text()
    late = fields.Boolean(compute='_compute_late') # TODO: review late

    def _compute_late(self):
        for rec in self.filtered(lambda r: not r.date_done):
            rec.late = fields.Date.from_string(rec.date_due) < date.today()
        for rec in self.filtered(lambda r: r.date_done):
            rec.late = fields.Date.from_string(rec.date_due) < fields.Date.from_string(rec.date_done)

    @api.model
    def create(self, vals):
        if 'name' not in vals or vals['name'] == '/':
            task_id = vals.get('house_task_id')
            sequence = False
            if task_id:
                task = self.env['house.task'].browse(task_id)
                sequence = task.sequence_id
            if sequence:
                vals['name'] = sequence.next_by_id()
        return super().create(vals)

    def action_done(self):
        self.write({
            'state': 'done',
            'date_done': fields.Date.today(),
        })

    def action_cancel(self):
        self.write({'state': 'cancel'})
