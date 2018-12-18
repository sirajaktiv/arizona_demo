# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProjectProgress(models.TransientModel):
    _name = "project.progress"
    _rec_name = "project_id"

    @api.model
    def default_get(self, default_fields):
        res = dict()
        project_rec = self.env['project.project'].browse(
            self._context.get('active_ids'))
        res['project_id'] = project_rec.id
        task_recs = self.env['project.task'].search(
            [('project_id', '=', project_rec.id)])

        task_stage_recs = project_rec.stage_ids
        if task_stage_recs:
            body = '''<table class="table table-striped"><thead>
                <tr style="font-weight:bold">
                <td>Stage Name</td>
                <td>Stage Percentage</td>
                <td>Completed Percentage</td></tr></thead><tbody>'''
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
                        completed_per += project_rec.project_task_stage_progress(
                            stage_total_percentage, task_rec, task_per)
                else:
                    completed_per += round(stage_total_percentage, 3)
                if completed_per > stage_total_percentage:
                    completed_per = round(stage_total_percentage, 3)
                total_completed_per += completed_per
                body_data = "<tr><td>" + stage_rec.name + "</td><td>" + \
                    str(round(stage_total_percentage, 2)) + \
                    "%</td><td>" + str(round(completed_per, 2)) + "%</td></tr>"
                body += body_data
            body += "<tr><td><b>Total</b></td><td><b>" + \
                str(100) + \
                "%</b></td><td><b>" + str(round(total_completed_per, 2)) + \
                "%</b></td></tr></tbody></table>"
            res['project_progress_records'] = body
        return res

    company_id = fields.Many2one(
        'res.company', string="Company", required=True,
        default=lambda self: self.env['res.company'].
        _company_default_get('project.progress'))
    project_id = fields.Many2one(
        'project.project', string="Project")
    project_progress_records = fields.Html(string="Project Progress Data")
