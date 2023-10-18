import logging

from odoo import models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    def _compute_l10n_ch_isr_valid(self):
        """Set as invalid."""
        for record in self:
            record.l10n_ch_isr_valid = False
