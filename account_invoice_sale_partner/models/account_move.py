import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    partner_sale_id = fields.Many2one(
        "res.partner",
        string="Sale Contact Address",
        compute="_compute_partner_sale_id",
        store=True,
    )

    @api.depends("partner_id")
    def _compute_partner_sale_id(self):
        for move in self:
            if move.partner_id:
                addr = move.partner_id.address_get(["sale"])
                move.partner_sale_id = addr["sale"]
            else:
                move.partner_sale_id = False
