import logging
import re

from odoo import models

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"


    def get_l10n_ch_qrr_number(self):
        super().get_l10n_ch_qrr_number()
        
        self.ensure_one()
        if self.partner_bank_id.l10n_ch_qr_iban and self.currency_id.name == "CHF" and self.name:
            invoice_ref = re.sub(r'[^\d]', '', self.name)
            return self._compute_qrr_number(invoice_ref)
        else:
            return False