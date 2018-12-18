# -*- coding: utf-8 -*-

from odoo import models, api


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.model
    def get_timesheet_entries(self, project_id):
        # Get timesheet entries to display in project dashboard.
        timesheet_recs = self.search([('project_id', '=', project_id)])
        project_manager_rec = self.env[
            'project.project'].browse(project_id).user_id
        employee_rec = self.env['hr.employee'].search(
            [('user_id', '=', project_manager_rec.id)])
        pm_line_recs = self.search(
            [('project_id', '=', project_id),
             ('employee_id', 'in', employee_rec.ids)])
        employee_ids = timesheet_recs.mapped('employee_id')
        timesheet_list = []
        for employee_id in employee_ids:
            if employee_id.id != employee_rec.id:
                total_hours = 0
                for ts in timesheet_recs:
                    if ts.employee_id.id == employee_id.id:
                        total_hours += ts.unit_amount
                timesheet_dict = {'name': employee_id.name,
                                  'unit_amount': total_hours}
                timesheet_list.append(timesheet_dict)
        for employee_id in employee_rec:
            total_hours = 0
            for ts in pm_line_recs:
                if ts.employee_id.id == employee_id.id:
                    total_hours += ts.unit_amount
            timesheet_dict = {'pm_name': employee_id.name,
                              'pm_unit_amount': total_hours}
            timesheet_list.append(timesheet_dict)
        return timesheet_list
