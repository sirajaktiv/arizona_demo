# -*- coding: utf-8 -*-
from odoo import api, fields, models
import os
_img_path = os.path.abspath(os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'static/src/img'))


class DmsDirectory(models.Model):
    _name = "dms.directory"

    @api.multi
    def count_directories(self):
        # count total sub directories of current directory.
        for res in self:
            res.total_child_directories = \
                self.env['dms.directory'].search_count(
                    [('parent_directory_id', '=', res.id)])

    name = fields.Char(string="Directory Name")
    user_id = fields.Many2one(
        'res.users', string="Directory User",
        default=lambda self: self.env.user)
    parent_directory_id = fields.Many2one(
        'dms.directory',
        string="Parent Directory",
        domain="[('user_id','=',uid),('id','!=',active_id)]",
        ondelete="cascade")
    child_ids = fields.One2many('dms.directory', 'parent_directory_id')
    total_child_directories = fields.Integer(compute="count_directories")
    res_model = fields.Char(string="Model")
    res_id = fields.Integer(string="Model ID")
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self:
                                 self.env['res.company'].
                                 _company_default_get('dms.directory'))

    @api.model
    def create(self, vals):
        rec = super(DmsDirectory, self).create(vals)
        if not vals.get('res_model'):
            rec.res_model = 'dms.directory'
            rec.res_id = rec.id
        return rec

    def check_child_ids(self, ids):
        # find sub directories ids
        child_ids_list = []
        for i in ids:
            if i.child_ids:
                child_ids_list.append(i.child_ids.ids)
        child_ids = [j for i in child_ids_list for j in i]
        return child_ids

    @api.multi
    def name_get(self):
        # this function append parent directory name before current directory
        # name.
        return [(value.id, "%s: %s"
                 % (value.parent_directory_id.name
                    if value.parent_directory_id.name
                    else "Root", value.name)) for value in self]

    @api.model
    def _create_directories(self):
        project_recs = self.env['project.project'].search([])
        self.create_directories(project_recs)

    def create_directories(self, project_recs):
        for project_rec in project_recs:
            project_dir = self.create(
                {'res_model': 'project.project',
                 'res_id': project_rec.id,
                 'company_id': self.env.user.company_id.id,
                 'parent_directory_id': False,
                 'name': project_rec.name})
            stage_recs = project_rec.stage_ids
            for stage_rec in stage_recs:
                stage_dir = self.create(
                    {'res_model': 'project.task.type',
                     'res_id': stage_rec.id,
                     'company_id': self.env.user.company_id.id,
                     'parent_directory_id': project_dir.id,
                     'name': stage_rec.name})
                task_recs = self.env['project.task'].search(
                    [('project_id', '=', project_rec.id),
                     ('parent_id', '=', False),
                     ('stage_id', '=', stage_rec.id)])
                for task_rec in task_recs:
                    task_dir = self.create(
                        {'res_model': 'project.task',
                         'res_id': task_rec.id,
                         'company_id': self.env.user.company_id.id,
                         'parent_directory_id': stage_dir.id,
                         'name': task_rec.name})
                    for stage_rec in stage_recs:
                        sub_stage_dir = self.create(
                            {'res_model': 'project.task.type',
                             'res_id': stage_rec.id,
                             'company_id': self.env.user.company_id.id,
                             'parent_directory_id': task_dir.id,
                             'name': stage_rec.name})
                        if task_rec.child_ids:
                            child_recs = task_rec.child_ids.with_context(
                                stage_id=stage_rec.id).filtered(
                                lambda t: t.stage_id.id ==
                                t._context['stage_id'])
                            for child_rec in child_recs:
                                self.create(
                                    {'res_model': 'project.task',
                                     'res_id': child_rec.id,
                                     'company_id': self.env.user.company_id.id,
                                     'name': child_rec.name,
                                     'parent_directory_id': sub_stage_dir.id})
