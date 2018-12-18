from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    task_id = fields.Many2one("project.task", string="Task")
