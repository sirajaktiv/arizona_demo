# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.multi
    def _compute_attached_docs_count(self):
        Attachment = self.env['ir.attachment']
        for task in self:
            task.doc_count = Attachment.search_count([
                ('res_model', '=', 'project.task'), ('res_id', '=', task.id)
            ])

    doc_count = fields.Integer(
        compute='_compute_attached_docs_count',
        string="Number of documents attached"
    )

    @api.multi
    def unlink(self):
        for task_rec in self:
            task_dir_rec = self.env['dms.directory'].search(
                [('res_model', '=', 'project.task'),
                 ('res_id', '=', task_rec.id)])
            task_dir_rec.unlink()
        return super(ProjectTask, self).unlink()

    @api.multi
    def write(self, vals):
        if not self._context.get('copy'):
            directory = self.env['dms.directory']
            for task_rec in self:
                task_dir_rec = directory.search(
                    [('res_model', '=', 'project.task'),
                     ('res_id', '=', task_rec.id)])
                if vals.get('name'):
                    task_dir_rec.write({'name': vals.get('name')})
                if vals.get('stage_id'):
                    stage_dir_recs = directory.search(
                        [('res_model', '=', 'project.task.type'),
                         ('res_id', '=', vals.get('stage_id'))])
                    if task_rec.parent_id:
                        task_dir = stage_dir_recs.mapped(
                            'parent_directory_id').with_context(
                            task_id=task_rec.parent_id.id).filtered(
                                lambda s: s.res_model ==
                                'project.task' and s.res_id ==
                                s._context['task_id'])
                        root_id = task_dir.child_ids.with_context(
                            stage_id=vals.get('stage_id')).filtered(
                            lambda s: s.res_id == s._context['stage_id'])
                    else:
                        project_dir = stage_dir_recs.mapped(
                            'parent_directory_id').with_context(
                            project_id=task_rec.project_id.id).filtered(
                            lambda s: s.res_model == 'project.project' and
                            s.res_id == s._context['project_id'])
                        root_id = project_dir.child_ids.with_context(
                            stage_id=vals.get('stage_id')).filtered(
                            lambda s: s.res_id == s._context['stage_id'])
                    task_dir_rec.write({'parent_directory_id': root_id.id})
        return super(ProjectTask, self).write(vals)

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        return super(ProjectTask, self.with_context({'copy': True})).copy(
            default)

    @api.model
    def create(self, vals):
        task_rec = super(ProjectTask, self).create(vals)
        dir_vals = {}
        parent_dir_recs = self.env['dms.directory'].search(
            [('res_model', '=', 'project.task.type'),
             ('res_id', '=', task_rec.stage_id.id)])
        if task_rec.parent_id:
            parent_dir_rec = parent_dir_recs.mapped(
                'parent_directory_id').with_context(
                task_id=task_rec.parent_id.id).filtered(
                lambda p: p.res_model == 'project.task' and
                p.res_id == p._context['task_id'])
            root_id = parent_dir_rec.child_ids.with_context(
                stage_id=task_rec.stage_id.id).filtered(
                lambda p: p.res_id == p._context['stage_id'])
        else:
            parent_dir_rec = parent_dir_recs.mapped(
                'parent_directory_id').with_context(
                project_id=task_rec.project_id.id).filtered(
                lambda p: p.res_model == 'project.project' and
                p.res_id == p._context['project_id'])
            root_id = parent_dir_rec.child_ids.with_context(
                stage_id=task_rec.stage_id.id).filtered(
                lambda p: p.res_id == p._context['stage_id'])
        dir_vals.update({'parent_directory_id': root_id.id})
        dir_vals = {'name': task_rec.name,
                    'res_id': task_rec.id,
                    'res_model': 'project.task',
                    'company_id': self.env.user.company_id.id}
        self.env['dms.directory'].create(dir_vals)
        return task_rec

    @api.multi
    def attachment_tree_view(self):
        self.ensure_one()
        domain = [
            ('res_model', '=', 'project.task'),
            ('res_id', '=', self.id)
        ]
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Documents are attached to the tasks and
                        issues of your project.</p><p>
                        Send messages or log internal notes with attachments to
                        link documents to your project.
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}"
            % (self._name, self.id)
        }
