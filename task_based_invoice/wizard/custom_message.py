from odoo import models, fields


class CustomMessage(models.TransientModel):
    _name = "custom.pop.message"

    name = fields.Char(readonly=True)
