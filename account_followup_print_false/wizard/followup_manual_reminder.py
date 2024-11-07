from odoo import fields, models


class FollowupManualReminder(models.TransientModel):
    _inherit = "account_followup.manual_reminder"

    print = fields.Boolean(default=False)
