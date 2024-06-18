from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    note_header = fields.Html()
    note_footer = fields.Html()
