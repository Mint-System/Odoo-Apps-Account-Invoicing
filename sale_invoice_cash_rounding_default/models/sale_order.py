import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_invoices(self, grouped=False, final=False, date=None):
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)
        company = self.env.company
        if company.invoice_cash_rounding_id:
            moves.update({"invoice_cash_rounding_id": company.invoice_cash_rounding_id})
        return moves
