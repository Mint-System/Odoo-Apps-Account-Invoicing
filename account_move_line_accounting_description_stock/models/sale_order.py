from odoo import models
import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        line = super()._prepare_invoice_line(**optional_values)
        move_line_ids = line["move_line_ids"]
        if move_line_ids:
            # Lookup last linked move in state done
            move_id = self.env['stock.move'].search([
                ('id','in',move_line_ids[0]),
                ('state','in',['done'])
            ],
            order='id desc',
            limit=1)
            # Copy move description to external name
            if move_id and move_id.description_picking:
               line["external_name"] = move_id.description_picking
        return line