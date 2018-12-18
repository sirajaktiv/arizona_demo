# -*- coding: utf-8 -*-
from odoo import api, models


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    @api.model
    def create(self, vals):
        task_type_rec = super(ProjectTaskType, self).create(vals)
        if task_type_rec.project_ids:
            self.create_stage_dir_inside_project(
                task_type_rec.project_ids, task_type_rec)
        return task_type_rec

    def create_stage_dir_inside_project(self, project_recs, task_type_rec):
        if project_recs:
            for project in project_recs:
                root_dir = self.env['dms.directory'].search(
                    [('res_model', '=', 'project.project'),
                     ('res_id', '=', project.id)])
                vals = {'name': task_type_rec.name,
                        'res_id': task_type_rec.id,
                        'res_model': 'project.task.type',
                        'parent_directory_id': root_dir.id,
                        'company_id': self.env.user.company_id.id}
                self.env['dms.directory'].create(vals)
                task_recs = self.env['project.task'].search(
                    [('project_id', '=', project.id),
                     ('parent_id', '=', False)])
                for task_rec in task_recs:
                    task_dir = self.env['dms.directory'].search(
                        [('res_model', '=', 'project.task'),
                         ('res_id', '=', task_rec.id)])
                    if task_dir:
                        vals = {'name': task_type_rec.name,
                                'res_id': task_type_rec.id,
                                'res_model': 'project.task.type',
                                'parent_directory_id': task_dir.id,
                                'company_id': self.env.user.company_id.id}
                        self.env['dms.directory'].create(vals)

    @api.multi
    def write(self, vals):
        res = super(ProjectTaskType, self).write(vals)
        dms_dir = self.env['dms.directory']
        for task_stage in self:
            if vals.get('name'):
                stage_dir_recs = dms_dir.search([
                    ('res_id', '=', task_stage.id),
                    ('res_model', '=', 'project.task.type')])
                stage_dir_recs.write({'name': vals.get('name')})
            if vals.get('project_ids'):
                project_recs = task_stage.project_ids
                project_dir_recs = dms_dir.search(
                    [('res_id', 'in', project_recs.ids),
                     ('res_model', '=', 'project.project')])
                project_dir_recs.unlink()
                self.env['dms.directory'].create_directories(project_recs)
        return res

    @api.multi
    def unlink(self):
        stage_dir_recs = self.env['dms.directory'].search(
            [('res_model', '=', 'project.task.type'),
             ('res_id', 'in', self.ids)])
        stage_dir_recs.unlink()
        return super(ProjectTaskType, self).unlink()
