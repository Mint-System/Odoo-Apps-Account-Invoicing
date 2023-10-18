import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    def set_position(self):
        get_positions_from_orders = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("account.get_positions_from_orders")
        )
        for move in self:
            position = 0
            for line in move.invoice_line_ids.filtered(
                lambda l: not l.display_type
            ).sorted("sequence"):
                if get_positions_from_orders and (
                    line.sale_line_ids or line.purchase_line_id
                ):
                    line._compute_get_position()
                    position = int(line.position)
                else:
                    position += 1
                    line.position = position

    @api.model
    def create(self, values):
        res = super().create(values)
        res.set_position()
        return res

    def write(self, values):
        res = super().write(values)
        self.set_position()
        return res


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    position = fields.Char(
        "Pos", compute="_compute_get_position", store=True, readonly=True
    )

    @api.depends("purchase_line_id", "sale_line_ids")
    def _compute_get_position(self):
        get_positions_from_orders = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("account.get_positions_from_orders")
        )
        for rec in self:
            if rec.sale_line_ids and get_positions_from_orders:
                rec.position = rec.sale_line_ids[0].position
            elif rec.purchase_line_id and get_positions_from_orders:
                rec.position = rec.purchase_line_id.position
            else:
                rec.position = 0
