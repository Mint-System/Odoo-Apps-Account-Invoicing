from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    note_header = fields.Html(string="Note header")
    note_footer = fields.Html(string="Note footer")
