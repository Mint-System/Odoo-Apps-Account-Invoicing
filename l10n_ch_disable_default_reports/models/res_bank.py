from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    def _eligible_for_qr_code(self, qr_method, debtor_partner, currency):
        """Create report only if it is being sent as mail."""
        if self.env.context.get('custom_layout') == 'mail.mail_notification_paynow':
            return False
        return super()._eligible_for_qr_code(qr_method, debtor_partner, currency)