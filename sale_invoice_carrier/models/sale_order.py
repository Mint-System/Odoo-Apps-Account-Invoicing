import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_invoices(self, grouped=False, final=False, date=None):
        _logger.warning("##### CALLED ")
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)
        _logger.warning(f"##### Moves: {moves}")

        # Get latest picking that is not cancelled and has a carrier set
        pickings = self.picking_ids.filtered(
            lambda p: p.state not in ["cancel"] and p.carrier_id
        )[:1]
        _logger.warning(f"##### Pickings: {pickings}")
        # Set carrier if picking has been found
        if pickings:
            _logger.warning(
                f"##### Picking Carrier: {pickings[0].carrier_id.id}, {pickings[0].carrier_id.name}"
            )
            # moves.update({"carrier_id": pickings[0].carrier_id.id})
            moves.write({"carrier_id": pickings[0].carrier_id.id})
        return moves
