# -*- coding: utf-8 -*-

from odoo import models, api, _
from odoo.exceptions import UserError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    @api.constrains('user_id')
    def check_user_id(self):
        user_recs = self.search([('id', '!=', self.id)]).mapped('user_id')
        if self.user_id.id in user_recs.ids:
            raise UserError(
                _("This User is already defined in other employee."))
