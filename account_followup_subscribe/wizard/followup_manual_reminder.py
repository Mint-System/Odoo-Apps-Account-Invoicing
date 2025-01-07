import logging

from odoo import models

_logger = logging.getLogger(__name__)


class FollowupManualReminder(models.TransientModel):
    _inherit = "account_followup.manual_reminder"

    def process_followup(self):
        res = super().process_followup()
        if self.email and self.template_id:
            subscriber_ids = self.template_id.get_subscriber_ids()
            if subscriber_ids:
                self.partner_id._message_subscribe(subscriber_ids.ids)
        return res
