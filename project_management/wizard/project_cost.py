# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProjectCost(models.TransientModel):
    _name = "project.cost"
    _rec_name = "project_id"

    @api.model
    def default_get(self, default_fields):
        res = dict()
        project_rec = self.env['project.project'].browse(
            self._context.get('active_ids'))
        analytic_line_recs = self.env['account.analytic.line'].search(
            [('project_id', '=', project_rec.id)])
        hr_expense_recs = self.env['hr.expense'].search(
            [('analytic_account_id', '=', project_rec.analytic_account_id.id)])
        hr_expense_total = sum(
            [expense.total_amount for expense in hr_expense_recs])
        res['project_id'] = project_rec.id
        res['overall_expenses'] = hr_expense_total
        cost = hr_expense_total
        for analytic_line_rec in analytic_line_recs:
            hour = str(analytic_line_rec.unit_amount).split('.')[0]
            minute = int(
                str(analytic_line_rec.unit_amount).split('.')[1]) * 10 / 6
            unit_amount = float(hour + '.' + str(int(minute)))
            cost += analytic_line_rec.employee_id.timesheet_cost * unit_amount
        res['total_cost'] = cost
        res['overall_timesheet_cost'] = cost - hr_expense_total
        return res

    company_id = fields.Many2one(
        'res.company', string="Company", required=True,
        default=lambda self: self.env['res.company'].
        _company_default_get('project.cost'))
    project_id = fields.Many2one(
        'project.project', string="Project")
    project_cost = fields.Monetary(
        related="project_id.overall_project_cost", string="Project Cost")
    currency_id = fields.Many2one(
        'res.currency', related='company_id.currency_id', readonly=True)
    overall_expenses = fields.Monetary(
        string="Overall Expenses")
    overall_timesheet_cost = fields.Monetary(string="Overall Timesheet Cost")
    total_cost = fields.Monetary(string="Total_cost")
