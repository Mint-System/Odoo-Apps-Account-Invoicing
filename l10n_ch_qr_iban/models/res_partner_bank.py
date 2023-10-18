import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    # def _check_qr_iban_range(self, iban):
    #     """OVERWRITE: All ibans are valid qr ibans"""
    #     if not iban or len(iban) < 9:
    #         return False
    #     return True

    @api.model
    def _compute_name_from_postal_number(self, partner_name, postal_number):
        """Do not prefix account name with 'ISR'."""
        res = super()._compute_name_from_postal_number(partner_name, postal_number)
        return res.replace("ISR ", "")
