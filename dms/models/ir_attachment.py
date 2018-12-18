# -*- coding: utf-8 -*-
from odoo import api, models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def get_documents(self):
        attachment_recs = self.search([
            ('res_model', 'in', ['project.project',
                                 'project.task', 'dms.directory'])
        ])
        att_list = []
        for attachment_rec in attachment_recs:
            if attachment_rec.res_model == 'project.project':
                directory_rec = self.env['dms.directory'].search(
                    [('res_id', '=', attachment_rec.res_id),
                     ('res_model', '=', 'project.project')])
                att_list.append({
                    'id': attachment_rec.id,
                    'name': attachment_rec.name,
                    'mimetype': attachment_rec.mimetype,
                    'dms_directory_id': directory_rec.id
                })
            elif attachment_rec.res_model == 'project.task':
                task_id = self.env['project.task'].browse(
                    [attachment_rec.res_id])
                directory_rec = self.env['dms.directory'].search([
                    ('res_id', '=', task_id.id),
                    ('res_model', '=', 'project.task')])
                if directory_rec:
                    att_list.append({
                        'id': attachment_rec.id,
                        'name': attachment_rec.name,
                        'mimetype': attachment_rec.mimetype,
                        'dms_directory_id': directory_rec.id
                    })
            else:
                directory_rec = self.env['dms.directory'].search(
                    [('res_id', '=', attachment_rec.res_id),
                     ('res_model', '=', 'dms.directory')])
                if directory_rec:
                    att_list.append({
                        'id': attachment_rec.id,
                        'name': attachment_rec.name,
                        'mimetype': attachment_rec.mimetype,
                        'dms_directory_id': directory_rec.id
                    })
        return att_list

    @api.model
    def create(self, vals):
        if not vals.get('res_model'):
            model = self._context.get('active_model')
            active_id = self._context.get('active_ids')
            if model and active_id:
                vals.update({'res_model': model, 'res_id': active_id[0]})
        if vals.get('res_model') == 'project.project':
            project_id = self.env['project.project'].browse([vals['res_id']])
            name = project_id.name + '_' + vals['datas_fname']
            vals.update({'name': name})
        if vals.get('res_model') == 'project.task':
            task_id = self.env['project.task'].browse([vals['res_id']])
            name = task_id.name + '_' + vals['datas_fname']
            vals.update({'name': name})
        return super(IrAttachment, self).create(vals)
