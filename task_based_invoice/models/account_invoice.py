from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    task_id = fields.Many2one('project.task', string="Tasks")
