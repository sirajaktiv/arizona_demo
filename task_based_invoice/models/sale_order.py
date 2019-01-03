from odoo import models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        order_ids = self.mapped('order_line').ids
        task_rec = self.env['project.task'].search(
            [('sale_line_id', 'in', order_ids)])
        if task_rec:
            invoice_vals.update({'task_id': task_rec.id})
        return invoice_vals
