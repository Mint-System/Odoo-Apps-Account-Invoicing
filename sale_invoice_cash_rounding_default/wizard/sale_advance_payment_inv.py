from odoo import models
import logging
_logger = logging.getLogger(__name__)


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        res = super()._prepare_invoice_values(order, name, amount, so_line)
        invoice_cash_rounding_id = self.env['ir.default'].get_model_defaults('account.move',condition='move_type=out_invoice').get('invoice_cash_rounding_id')
        if invoice_cash_rounding_id:
            res["invoice_cash_rounding_id"] = invoice_cash_rounding_id
        # _logger.warning(["ADDED CASH ROUNDING", invoice_cash_rounding_id])
        return res
