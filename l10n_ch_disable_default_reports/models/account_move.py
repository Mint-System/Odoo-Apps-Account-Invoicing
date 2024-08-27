import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    enable_ch_qr_code = fields.Boolean(
        default=True,
    )

    def _compute_l10n_ch_qr_is_valid(self):
        """Set QR code validity based on enable_ch_qr_code field."""
        result = super()._compute_l10n_ch_qr_is_valid()
        for move in self:
            if not move.enable_ch_qr_code:
                move.l10n_ch_qr_is_valid = False
        return result
