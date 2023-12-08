import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        res = super()._prepare_invoice_values(order, name, amount, so_line)
        company = self.env.company
        if company.invoice_cash_rounding_id:
            res["invoice_cash_rounding_id"] = company.invoice_cash_rounding_id
        return res
