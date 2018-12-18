# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Project(models.Model):
    _inherit = "project.project"

    @api.model
    def get_current_project_details(self, project_id):
        project_rec = self.sudo().search_read([('id', 'in', project_id)])
        for key in project_rec[0]:
            if key != 'progress_total':
                if not project_rec[0][key]:
                    project_rec[0].update({key: ''})
            if key == 'progress_total':
                project_rec[0].update({key: round(project_rec[0][key], 2)})
        project_rec[0].update({'user_id': project_rec[0]['user_id'][1]})
        return project_rec

    @api.model
    def get_stage_progress(self, project_id):
        project_rec = self.sudo().browse(project_id)
        res = {}
        task_stage_recs = project_rec.stage_ids
        if task_stage_recs:
            total_completed_per = 0
            stage_total_percentage = 100 / len(task_stage_recs)
            for stage_rec in task_stage_recs:
                completed_per = 0
                task_recs = self.env['project.task'].search(
                    [('project_id', '=', project_rec.id),
                     ('stage_id', '=', stage_rec.id),
                     ('parent_id', '=', False)])
                if task_recs:
                    task_per = stage_total_percentage / len(task_recs)
                    for task_rec in task_recs:
                        completed_per = completed_per + \
                            project_rec.project_task_stage_progress(
                                stage_total_percentage, task_rec, task_per)
                else:
                    completed_per += round(stage_total_percentage, 3)
                if completed_per > stage_total_percentage:
                    completed_per = round(stage_total_percentage, 3)
                total_completed_per += completed_per
                res.update(
                    {stage_rec.id: [stage_rec.name,
                                    round(stage_total_percentage, 2),
                                    round(completed_per, 2)]})
            res.update(
                {0: ["Total", 100, round(total_completed_per, 2)]})
        return res

    @api.model
    def _deactivate_no_update_project_rules(self):
        self._cr.execute(
            "UPDATE ir_model_data SET noupdate='f' WHERE name='task_visibility_rule' or name='project_public_members_rule';")
        self._cr.execute(
            "UPDATE ir_rule SET active='f' where name='Project/Task: employees:follow required for follower-only projects'or name = 'Project: employees: following required for follower-only projects';")

    @api.multi
    def get_project_progress(self):
        for project_rec in self:
            stage_recs = project_rec.stage_ids
            if stage_recs:
                stage_per = 100 / len(stage_recs)
                for stage_rec in stage_recs:
                    task_recs = self.env['project.task'].search(
                        [('project_id', '=', project_rec.id),
                         ('stage_id', '=', stage_rec.id),
                         ('parent_id', '=', False)])
                    if task_recs:
                        task_per = stage_per / len(task_recs)
                        for task_rec in task_recs:
                            task_progress = self.project_task_stage_progress(
                                stage_per, task_rec, task_per)
                            project_rec.progress_total += task_progress
                    else:
                        project_rec.progress_total += stage_per
                if project_rec.progress_total > 100:
                    project_rec.progress_total = 100

    def project_task_stage_progress(self, stage_per, task_rec, task_per):
        if task_rec.child_ids:
            total_task_per = sum(
                [task.task_progress for task in task_rec.child_ids])
            progress = (total_task_per * 100) / (len(task_rec.child_ids) * 100)
            task_progress = progress * task_per / 100
            return round(task_progress, 3)
        else:
            task_progress = task_rec.task_progress * task_per / 100
            return round(task_progress, 3)

    @api.multi
    def change_colore_on_kanban(self):
        for record in self:
            color = '#000'
            if record.total_cost <= 50:
                color = 'blue'
            elif record.total_cost <= 60:
                color = '#00ff00'
            elif record.total_cost <= 70:
                color = 'orange'
            elif record.total_cost > 70:
                color = 'red'
            else:
                color = 'red'
            record.button_color = color

    @api.multi
    def get_total_cost(self):
        for project_rec in self:
            try:
                analytic_line_recs = self.env['account.analytic.line'].search(
                    [('project_id', '=', project_rec.id)])
                hr_expense_recs = self.env['hr.expense'].search(
                    [('analytic_account_id', '=',
                        project_rec.analytic_account_id.id)])
                hr_expense_total = sum(
                    [expense.total_amount for expense in hr_expense_recs])
                cost = hr_expense_total
                for analytic_line_rec in analytic_line_recs:
                    hour = str(analytic_line_rec.unit_amount).split('.')[0]
                    minute = int(
                        str(analytic_line_rec.unit_amount)
                        .split('.')[1]) * 10 / 6
                    unit_amount = float(hour + '.' + str(int(minute)))
                    cost += analytic_line_rec.employee_id.timesheet_cost * \
                        unit_amount
                project_rec.total_cost = (
                    cost / project_rec.overall_project_cost) * 100
            except Exception:
                pass

    overall_project_cost = fields.Monetary(
        store=True, currency_field='currency_id', default=0.0)
    currency_id = fields.Many2one(
        'res.currency', related='company_id.currency_id', readonly=True)
    total_cost = fields.Integer(compute='get_total_cost')
    progress_total = fields.Float(compute='get_project_progress')
    button_color = fields.Char(
        'Button Color', compute="change_colore_on_kanban")
    project_goal = fields.Char(string="Project Goal")
    user_ids = fields.Many2many('res.users', string="Employees")
    project_dead_line = fields.Date(string="End Date")
    project_start_date = fields.Date(string="Start Date")
    stage_ids = fields.Many2many(
        'project.task.type', string="Stages")
    priority = fields.Selection(
        [('high', 'High'), ('medium', 'Medium'), ('low', 'Low')],
        string="Priority")
    project_sponser_id = fields.Many2one(
        'res.partner', string="Project Sponser")
    project_owner_id = fields.Many2one('res.partner', string="Project Owner")
    contract_no = fields.Char(string="Contract No.")
    notes_action = fields.Text()
    issue_risk = fields.Text()
    solution = fields.Text()

    @api.model
    def create(self, vals):
        project_rec = super(Project, self).create(vals)
        project_rec.stage_ids.write(
            {'project_ids': [(4, project_rec.id)]})
        return project_rec

    def filter_stage_ids(self, stage_recs, project_id):
        stage_ids = []
        for stage_rec in stage_recs:
            if project_id.id not in stage_rec.project_ids.ids:
                stage_ids.append(stage_rec.id)
        return stage_ids

    @api.multi
    def write(self, vals):
        res = super(Project, self).write(vals)
        for project_rec in self:
            if vals.get('stage_ids'):
                stage_ids = self.filter_stage_ids(project_rec.stage_ids,
                                                  project_rec)
                if stage_ids:
                    stage_recs = self.env[
                        'project.task.type'].browse(stage_ids)
                    stage_recs.write(
                        {'project_ids': [(4, project_rec.id)]})
        return res
