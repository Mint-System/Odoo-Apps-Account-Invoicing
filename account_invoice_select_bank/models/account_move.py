from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('currency_id')
    def _onchange_currency_id(self):
        self._compute_partner_bank_id()

    @api.depends('bank_partner_id')
    def _compute_partner_bank_id(self):
        super()._compute_partner_bank_id()
        for move in self:
            bank_ids = move.bank_partner_id.bank_ids.filtered(lambda bank: bank.company_id is False or bank.company_id == move.company_id)
            bank_currency_ids = bank_ids.filtered(lambda bank: bank.currency_id == move.currency_id)
            if bank_currency_ids:
                move.partner_bank_id = bank_currency_ids[0]
            else:
                move.partner_bank_id = bank_ids and bank_ids[0]