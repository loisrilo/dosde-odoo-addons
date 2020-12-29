# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta, date

from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError


class HouseTask(models.Model):
    _name = "house.task"
    _description = "House Task"

    DEFAULT_PYTHON_CODE = """# Available variables:
    #  - env: Odoo Environment on which the action is triggered
    #  - model: Odoo Model of the record on which the action is triggered; is a void recordset
    #  - record: record on which the action is triggered; may be be void
    #  - records: recordset of all records on which the action is triggered in multi-mode; may be void
    #  - time, datetime, dateutil, timezone: useful Python libraries
    #  - log: log(message, level='info'): logging function to record debug information in ir.logging table
    #  - Warning: Warning Exception to use with raise
    # To return the next assigned user, assign: next = res.user record.\n\n\n\n"""

    name = fields.Char(required=True)
    description = fields.Html()
    active = fields.Boolean(default=True)
    user_ids = fields.Many2many(
        comodel_name="res.users",
        string="Users",
        required=True,
    )
    period_min = fields.Integer(
        string="Days to Next",
        required=True,
        help="The minimum days until next turn is required.",
    )
    period_max = fields.Integer(
        string="Days to Due",
        required=True,
        help="The number of days until next turn is considered late.",
    )
    python_code = fields.Text(
        string='Python Code', groups='base.group_system',
        default=DEFAULT_PYTHON_CODE,
        help="Write Python code that will recide the next user assigned to"
             "the task.",
    )
    code_prefix = fields.Char(
        string="Prefix for Task Turns",
    )
    sequence_id = fields.Many2one(
        comodel_name="ir.sequence", string="Task Sequence",
        help="This field contains the information related to the numbering "
             "of the turns of this task.",
        copy=False, readonly=True,
    )
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Name must be unique"),
    ]

    @api.model
    def _prepare_ir_sequence(self, prefix):
        """Prepare the vals for creating the sequence
        :param prefix: a string with the prefix of the sequence.
        :return: a dict with the values.
        """
        vals = {
            "name": "Housekeeping Task " + prefix,
            "code": "house.task.turn - " + prefix,
            "padding": 5,
            "prefix": prefix,
            "company_id": False,
        }
        return vals

    def write(self, vals):
        prefix = vals.get("code_prefix")
        if prefix:
            for rec in self:
                if rec.sequence_id:
                    rec.sudo().sequence_id.prefix = prefix
                else:
                    seq_vals = self._prepare_ir_sequence(prefix)
                    rec.sequence_id = self.env["ir.sequence"].create(seq_vals)
        return super().write(vals)

    @api.model
    def create(self, vals):
        prefix = vals.get("code_prefix")
        if prefix:
            seq_vals = self._prepare_ir_sequence(prefix)
            sequence = self.env["ir.sequence"].create(seq_vals)
            vals["sequence_id"] = sequence.id
        return super().create(vals)

    def _evaluate_python_code(self):
        eval_ctx = {'rec': self, 'env': self.env}
        try:
            safe_eval(
                self.python_code, mode="exec",
                nocopy=True, globals_dict=eval_ctx)
        except Exception as error:
            raise UserError(_(
                "Error evaluating python code.\n %s") % error)
        return eval_ctx.get('next')

    def generate(self):
        turn_model = self.env['house.task.turn']
        for rec in self:
            pending = turn_model.search([
                ('house_task_id', '=', rec.id),
                ('state', '=', 'pending')])
            if pending:
                continue

            last = turn_model.search([
                ('house_task_id', '=', rec.id),
                ('state', '=', 'done')], order='date_done desc', limit=1)
            if last and fields.Date.from_string(last.date_done) + timedelta(
                    days=rec.period_min) > date.today():
                continue

            assigned_to = rec._evaluate_python_code()
            if not assigned_to:
                continue

            turn_model.create({
                'house_task_id': rec.id,
                'date_due': fields.Date.from_string(last.date_done) +
                timedelta(days=rec.period_max),
                'user_id': assigned_to.id,
            })
