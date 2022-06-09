from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    comment = fields.Text(tracking=True)
