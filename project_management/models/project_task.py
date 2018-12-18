# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def get_progress_task(self, project_id):
        task_recs = self.env['project.task'].search(
            [('project_id', '=', project_id)])
        not_started = task_recs.search_count(
            [('id', 'in', task_recs.ids),
             ('task_completion_date', '=', False),
             ('member_status', '=', 'to_do')])
        lately_task_recs = self.env['project.task'].search(
            [('project_id', '=', project_id),
             ('task_completion_date', '!=', False),
             ('member_status', '=', 'done')])
        in_progress_task = self.env['project.task'].search_count(
            [('project_id', '=', project_id),
             ('member_status', '=', 'in_progress')])
        lately_completed = 0
        completed = 0
        if lately_task_recs:
            lately_completed = len(lately_task_recs.filtered(
                lambda t: t.task_completion_date > t.date_deadline).ids)
            completed = len(lately_task_recs.filtered(
                lambda t: t.task_completion_date <= t.date_deadline and
                t.task_completion_date).ids)
        pichart_dict = {
            'task_status': ['Lately Completed',
                            'Not Started',
                            'Completed',
                            'In Progress'],
            'task_progress': [lately_completed,
                              not_started,
                              completed,
                              in_progress_task]}
        return pichart_dict

    @api.model
    def get_task_not_completed(self, project_id):
        task_recs = self.env['project.task'].search(
            [('project_id', '=', project_id)])
        not_started = task_recs.search_count(
            [('id', 'in', task_recs.ids),
             ('task_completion_date', '=', False),
             ('member_status', '=', 'to_do')])
        lately_task_recs = self.env['project.task'].search(
            [('project_id', '=', project_id),
             ('task_completion_date', '!=', False)])
        lately_completed_per = 0
        not_started_per = 0
        if lately_task_recs:
            lately_completed = len(lately_task_recs.filtered(
                lambda t: t.task_completion_date > t.date_deadline).ids)
            total_task = lately_completed + not_started
            if total_task != 0:
                lately_completed_per = lately_completed / total_task * 100
            if not_started > 0:
                not_started_per = not_started / total_task * 100
        if not lately_task_recs:
            total_task = len(task_recs)
            if not_started > 0:
                not_started_per = not_started / total_task * 100
        status_dict = {'lately_completed': lately_completed_per,
                       'not_started': not_started_per}
        return status_dict

    kanban_state = fields.Selection([
        ('normal', 'Grey'),
        ('done', 'Green'),
        ('blocked', 'Red'),
        ('progress', 'Yellow')], string='Kanban State',
        copy=False, default='normal', required=True,
        help='''A task's kanban state indicates special
            situations affecting it:\n
            * Grey is the default situation\n
            * Red indicates something is preventing the progress of this task\n
            * Green indicates the task is ready to be
            pulled to the next stage''')
    task_completion_date = fields.Date(string="Completion Date")
    task_description = fields.Text()
    task_progress = fields.Float(string="Progress")
    task_stage_progress = fields.Float(
        string="Stage Progress", compute="_onchange_task_progress")
    member_status = fields.Selection(
        [('to_do', 'To Do'), ('in_progress', 'In Progress'),
         ('done', 'Done')])
    legend_inprogress = fields.Char(
        related='stage_id.legend_inprogress', string='In Progress',
        readonly=True, related_sudo=False)
    vendor_partner_id = fields.Many2one('res.partner', string="Vendor",
                                        domain=[('supplier', '=', True)])

    @api.depends('stage_id', 'kanban_state')
    def _compute_kanban_state_label(self):
        for task in self:
            if task.kanban_state == 'normal':
                task.kanban_state_label = task.legend_normal
            elif task.kanban_state == 'blocked':
                task.kanban_state_label = task.legend_blocked
            elif task.kanban_state == 'progress':
                task.kanban_state_label = task.legend_inprogress
            else:
                task.kanban_state_label = task.legend_done

    @api.multi
    @api.onchange('task_progress')
    def _change_task_progress(self):
        # Change member status onchange of task progress
        # And Increase or Decrese stage percentage on chnage of task progress.
        for task_rec in self:
            if task_rec.task_progress == 0:
                task_rec.member_status = "to_do"
            if task_rec.task_progress > 0:
                task_rec.member_status = "in_progress"
            if task_rec.task_progress >= 100:
                task_rec.member_status = "done"

    @api.depends('task_progress', 'stage_id')
    def _onchange_task_progress(self):
        for task_rec in self:
            if task_rec.project_id.stage_ids:
                stage_per = 100 / len(task_rec.project_id.stage_ids)
                stage_rec = task_rec.stage_id
                task_count = self.env['project.task'].search_count(
                    [('project_id', '=', task_rec.project_id.id),
                     ('stage_id', '=', stage_rec.id),
                     ('parent_id', '=', False)])
                if task_count == 0:
                    task_rec.task_stage_progress = 0
                    return 0
                if task_rec.stage_id:
                    project_rec = task_rec.project_id
                    per_one_task_per = stage_per / task_count
                    task_stage_prgs = project_rec.project_task_stage_progress(
                        stage_per, task_rec, per_one_task_per)
                    task_rec.task_stage_progress = task_stage_prgs

    @api.constrains('task_progress')
    def _task_progress_cons(self):
        if self.task_progress > 100:
            raise ValidationError(_("Please enter in range 0 - 100."))

    @api.multi
    def action_create_purchase_order(self):
        purchase = self.env['purchase.order']
        pol = self.env['purchase.order.line']
        product = self.env['product.product']
        for task_rec in self:
            if not task_rec.planned_hours:
                raise UserError(_("Please fill Initially Planned Hours."))
            if not task_rec.vendor_partner_id:
                raise ValidationError(_("Please select vendor of task."))
            purchase_rec = purchase.create(
                {'partner_id': task_rec.vendor_partner_id.id,
                 'task_id': task_rec.id,
                 'date_order': str(datetime.today()),
                 'state': 'draft'
                 })
            uom_rec = self.env['product.uom'].search(
                [('name', '=', 'Hour(s)')])
            product_rec = product.create(
                {'name': task_rec.name,
                 'type': 'service',
                 'purchase_ok': True,
                 'sale_ok': True,
                 'service_tracking': 'task_global_project',
                 'project_id': task_rec.project_id.id,
                 'categ_id': 4})
            pol.create({'product_id': product_rec.id,
                        'product_qty': task_rec.planned_hours,
                        'order_id': purchase_rec.id,
                        'name': task_rec.name,
                        'date_planned': str(datetime.today()),
                        'product_uom': uom_rec.id,
                        'price_unit': 0})
        return {
            'name': 'Status',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'custom.pop.message',
            'target': 'new',
            'context': {'default_name': "Purchase order created successfully."}
        }

    def change_color(self, vals):
        completion_date = self.task_completion_date
        if vals.get('task_completion_date'):
            completion_date = vals['task_completion_date']
        if not completion_date:
            completion_date = str(datetime.now().date())
        if vals.get('member_status'):
            if vals['member_status'] == 'done':
                if vals.get('date_deadline'):
                    if vals['date_deadline'] > completion_date:
                        vals.update({'color': 10, 'kanban_state': 'done'})
                if not vals.get('date_deadline'):
                    if self.date_deadline > completion_date:
                        vals.update({'color': 10, 'kanban_state': 'done'})
                    else:
                        vals.update({'color': 10, 'kanban_state': 'blocked'})
            if vals['member_status'] == 'to_do':
                vals.update({'color': 1, 'kanban_state': 'normal'})
            if vals['member_status'] == 'in_progress':
                vals.update({'color': 3, 'kanban_state': 'progress'})
        if vals.get('stage_id'):
            vals.update({'kanban_state': self.kanban_state})
        return vals

    @api.multi
    def write(self, vals):
        for task in self:
            if self.env.user.has_group('project.group_project_manager'):
                vals = task.change_color(vals)
            else:
                if (vals.get('task_progress') and
                        vals.get('member_status') and len(vals) <= 2):
                    vals = task.change_color(vals)
                else:
                    raise Warning(_('You can not change this record.'))
        return super(ProjectTask, self).write(vals)
