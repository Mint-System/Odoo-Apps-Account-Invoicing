import logging
from odoo import _, api, fields, models
_logger = logging.getLogger(__name__)


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'
    
    def _check_qr_iban_range(self, iban):
        """OVERWRITE: All ibans are valid qr ibans"""
        if not iban or len(iban) < 9:
            return False
        return True