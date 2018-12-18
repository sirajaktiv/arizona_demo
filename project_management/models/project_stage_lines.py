# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import Warning


class ProjectStageLines(models.Model):
    _name = 'project.stage.lines'
    _rec_name = 'project_task_type_id'

    project_task_type_id = fields.Many2one(
        'project.task.type', string="Stage")
    stage_per = fields.Float(string="Stage Percentage")
    project_id = fields.Many2one('project.project', string="Project")
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env[
                                     'res.company']._company_default_get())

    @api.model
    def create(self, vals):
        lines = self.search([('project_id', '=', vals['project_id'])])
        if lines:
            sum_stage_per = sum([line.stage_per for line in lines])
            if sum_stage_per + vals['stage_per'] > 100:
                raise Warning(
                    _('Project stage percentage should be less or equal to 100.'))
            else:
                return super(ProjectStageLines, self).create(vals)
        else:
            return super(ProjectStageLines, self).create(vals)
