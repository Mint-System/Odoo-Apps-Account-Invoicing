from odoo import models
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_invoices(self, grouped=False, final=False, date=None):
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)
        invoice_cash_rounding_id = self.env['ir.default'].get_model_defaults('account.move',condition='move_type=out_invoice').get('invoice_cash_rounding_id')
        if invoice_cash_rounding_id:
            moves.invoice_cash_rounding_id = invoice_cash_rounding_id
        # _logger.warning(["ADDED CASH ROUNDING", invoice_cash_rounding_id])
        return moves
