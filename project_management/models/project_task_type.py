# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    legend_inprogress = fields.Char('Yello kanaban label', default=lambda s: _(
        'In Progress'), translate=True, required=True)

    @api.model
    def create(self, vals):
        task_type_rec = super(ProjectTaskType, self).create(vals)
        if self._context.get('active_model') == 'project.project':
            project_id = self._context.get('active_id')
            project_rec = self.env['project.project'].browse([project_id])
            project_rec.stage_ids = [(4, task_type_rec.id)]
        task_type_rec.project_ids.write({'stage_ids': [(4, task_type_rec.id)]})
        return task_type_rec

    # @api.multi
    # def write(self, vals):
    #     for task_type_rec in self:
    #         if vals.get('project_ids'):
    #             project_recs = self.env['project.project'].search(
    #                 [('stage_ids', 'in', task_type_rec.ids)])
    #             project_recs.write({'stage_ids': [(2, task_type_rec.id)]})
    #             projects = self.env['project.project'].browse(
    #                 vals.get('project_ids')[0][2])
    #             projects.write({'stage_ids': [[(4, task_type_rec.id)]]})
    #     return super(ProjectTaskType, self).write(vals)
