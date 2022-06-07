from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_invoice_id = fields.Many2one(
        "res.partner",
        string="Invoice Address",
        readonly=True,
        states={"draft": [("readonly", False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        super()._onchange_partner_id()
        if not self.partner_id:
            self.partner_invoice_id = False
            return

        addr = self.partner_id.address_get(['invoice'])
        self.update({
            'partner_invoice_id': addr['invoice']
        })