import logging

from odoo import models

_logger = logging.getLogger(__name__)


class AccountFollowupReport(models.AbstractModel):
    _inherit = "account.followup.report"

    def _send_email(self, options):
        res = super()._send_email(options)
        partner_id = self.env["res.partner"].browse(options.get("partner_id"))
        if partner_id:
            followup_line = options.get("followup_line", partner_id.followup_line_id)
            if followup_line:
                template_id = options.get("mail_template") or followup_line.mail_template_id
                if template_id:
                    subscriber_ids = template_id.get_subscriber_ids()
                    if subscriber_ids:
                        partner_id._message_subscribe(subscriber_ids.ids)
        return res
