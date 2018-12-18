# -*- coding: utf-8 -*-
from odoo import api, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    @api.model
    def create(self, vals):
        project_rec = super(ProjectProject, self).create(vals)
        self.env['dms.directory'].create(
            {'name': project_rec.name,
             'company_id': self.env.user.company_id.id,
             'res_model': 'project.project',
             'res_id': project_rec.id})
        return project_rec

    @api.multi
    def unlink(self):
        dms_recs = self.env['dms.directory'].search(
            [('res_model', '=', 'project.project'),
             ('res_id', '=', self.id)])
        dms_recs.unlink()
        return super(ProjectProject, self).unlink()

    @api.multi
    def write(self, vals):
        res = super(ProjectProject, self).write(vals)
        for project in self:
            if vals.get('name'):
                dms_rec = self.env['dms.directory'].search(
                    [('res_model', '=', 'project.project'),
                     ('res_id', 'in', self.ids)])
                dms_rec.write({'name': vals.get('name')})
            if vals.get('stage_ids'):
                project_dir_recs = self.env['dms.directory'].search(
                    [('res_id', '=', project.id),
                     ('res_model', '=', 'project.project')])
                project_dir_recs.unlink()
                self.env['dms.directory'].create_directories(project)
        return res
