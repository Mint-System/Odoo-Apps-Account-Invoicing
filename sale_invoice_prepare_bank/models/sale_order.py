from odoo import models
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        res = super()._prepare_invoice()      
        company = self.env.company or self.company_id  
        bank_ids = company.partner_id.bank_ids.filtered(lambda bank: bank.company_id is False or bank.company_id == company)
        bank_currency_ids = bank_ids.filtered(lambda bank: bank.currency_id == self.currency_id)
        if bank_currency_ids:
            res["partner_bank_id"] = bank_currency_ids[0].id
        else:
            res["partner_bank_id"] = bank_ids and bank_ids[0].id
        return res