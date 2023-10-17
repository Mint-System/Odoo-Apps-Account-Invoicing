import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange("currency_id")
    def _onchange_currency_id(self):
        self._compute_partner_bank_id()

    @api.depends("bank_partner_id")
    def _compute_partner_bank_id(self):
        res = super()._compute_partner_bank_id()
        for move in self:
            bank_currency_id = move.bank_partner_id.bank_ids.filtered(
                lambda bank: bank.currency_id == move.currency_id
            )[:1]
            if bank_currency_id:
                move.partner_bank_id = bank_currency_id[0]
            else:
                move.partner_bank_id = False
        return res