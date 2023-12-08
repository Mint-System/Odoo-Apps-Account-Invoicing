from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    comment = fields.Text(tracking=True)
