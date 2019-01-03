from odoo import api, fields, models, _
from odoo.exceptions import UserError


class InvoiceTaskRel(models.TransientModel):
    _name = "invoice.task.rel"

    def get_activ_tasks(self):
        task_ids = self._context.get('active_ids')
        return self.env['project.task'].browse(task_ids)

    task_ids = fields.Many2many('project.task', string="Tasks",
                                default=get_activ_tasks, required=True)

    def check_task_recs(self, task_recs):
        stages = task_recs.mapped('stage_id')
        invoice = self.env['account.invoice'].search(
            [('task_id', 'in', task_recs.ids)])
        if len(stages) > 2:
            raise UserError(_("Select only done stages."))
        if 'Done' != stages.name:
            raise UserError(_("Select only done stages."))
        task_ids = task_recs.filtered(lambda l: not l.product_id)
        if task_ids:
            raise UserError(_("Please select product in Task."))
        customer_ids = task_recs.filtered(lambda l: not l.partner_id)
        if customer_ids:
            raise UserError(_("Please select customer in Task."))
        if invoice:
            raise UserError(_("Task invoice already created."))

    @api.multi
    def action_validate_task(self):
        invoice = self.env['account.invoice']
        invoice_line = self.env['account.invoice.line']
        for rec in self:
            self.check_task_recs(rec.task_ids)
            for task in rec.task_ids:
                if not task.sale_line_id:
                    origin = task.name
                    partner = task.partner_id
                    product = task.product_id
                    vals = {
                        'partner_id': partner.id,
                        'state': 'draft',
                        'task_id': task.id,
                        'account_id': partner.property_account_receivable_id.id,
                        'origin': origin
                    }
                    invoice_rec = invoice.create(vals)
                    company = invoice_rec.company_id
                    type = invoice_rec.type
                    fpos = invoice_rec.fiscal_position_id
                    account = invoice_line.get_invoice_line_account(
                        type, product, fpos, company)
                    vals = {
                        'invoice_id': invoice_rec.id,
                        'product_id': task.product_id.id,
                        'quantity': task.planned_hours,
                        'price_unit': task.product_id.lst_price,
                        'name': task.product_id.name,
                        'account_id': account.id,
                        'uom_id': task.product_id.uom_id.id}
                    invoice_line.create(vals)
                if task.sale_line_id:
                    order = task.sale_line_id.order_id
                    order.action_invoice_create(final=True)
        return {
            'name': 'Status',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'custom.pop.message',
            'target': 'new',
            'context': {'default_name': "Invoices created successfully."}
        }
