from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = "project.task"

    product_id = fields.Many2one('product.product', string="Product",
                                 domain=[('type', '=', 'service')],
                                 related="sale_line_id.product_id")
