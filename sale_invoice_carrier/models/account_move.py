import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends("invoice_line_ids.sale_line_ids.order_id.picking_ids.carrier_id")
    def _compute_carrier_id(self):
        for move in self:
            carrier = False

            # Find related sale order (via invoice lines → sale lines → order)
            sale_orders = move.invoice_line_ids.mapped("sale_line_ids.order_id")

            if sale_orders:
                # Collect all carriers from all pickings of all related sale orders
                pickings = sale_orders.mapped("picking_ids")
                carriers = pickings.mapped("carrier_id")
                carrier = carriers[0] if carriers else False

            move.carrier_id = carrier
