import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    partner_invoice_id = fields.Many2one(
        "res.partner",
        string="Invoice Address",
        readonly=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        compute="_compute_partner_invoice_id",
        store=True,
    )

    @api.depends("partner_id")
    def _compute_partner_invoice_id(self):
        for record in self:
            if not record.partner_id:
                record.partner_invoice_id = False
            else:
                addr = record.partner_id.address_get(["invoice"])
                record.partner_invoice_id = addr.get("invoice", False)
