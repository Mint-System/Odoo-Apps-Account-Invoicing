from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    picking_ids = fields.Many2many('stock.picking', compute='_compute_picking_ids')

    def _compute_picking_ids(self):
        for rec in self:
            picking_ids = []

            for line in rec.sale_line_ids:
                for move in line.move_ids:
                    picking_ids.append(move.picking_id.id)

            rec.picking_ids = self.env['stock.picking'].search([('id', 'in', picking_ids)])
