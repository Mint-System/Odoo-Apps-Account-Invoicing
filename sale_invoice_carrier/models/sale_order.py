from odoo import models
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_invoices(self, grouped=False, final=False, date=None):
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)

        # Get latest picking that is not cancelled and has a carrier set
        pickings = self.picking_ids.filtered(lambda p: p.state not in ['cancel'] and p.carrier_id)[:1]
        # Set carrier if picking has been found
        if pickings:
            moves.update({
                'carrier_id': pickings[0].carrier_id.id
            })
        return moves
