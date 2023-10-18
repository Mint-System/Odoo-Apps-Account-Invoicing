from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_bank_id = fields.Many2one(compute="_compute_partner_bank_id", store=True)

    @api.onchange('currency_id')
    def _onchange_currency_id(self):
        self._compute_partner_bank_id()

    @api.depends('bank_partner_id')
    def _compute_partner_bank_id(self):
        for move in self:
            bank_id = move.bank_partner_id.bank_ids.filtered(lambda bank: bank.currency_id == move.currency_id)[:1]
            if bank_id:
                move.partner_bank_id = bank_id
            else:
                move.partner_bank_id = False