import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    enable_ch_qr_code = fields.Boolean(string="Enable Swiss QR-bill", help="Enable to print the swiss QR-bill.")

    @api.depends("enable_ch_qr_code")
    def _compute_l10n_ch_qr_is_valid(self):
        super()._compute_l10n_ch_qr_is_valid()
        for move in self:
            if not move.enable_ch_qr_code:
                move.l10n_ch_is_qr_valid = False
