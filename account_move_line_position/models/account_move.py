from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    position = fields.Integer("Pos", compute='_compute_get_position')

    def _compute_get_position(self):
        _logger.warning(self)
        for rec in self:
            if rec.sale_line_ids:
                rec.position = rec.sale_line_ids[0].position
            # if rec.move_id.sale_order_id:
            #     rec.position = rec.move_id.sale_order_id.get_position(rec.product_id, rec.quantity)
            elif rec.purchase_line_id:
                rec.position = rec.purchase_line_id.position
            # elif rec.purchase_order_id:
            #     rec.position = rec.purchase_order_id.get_position(rec.product_id, rec.quantity)
            else:
                rec.position = 0
