from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    note_header = fields.Html()
    note_footer = fields.Html()
