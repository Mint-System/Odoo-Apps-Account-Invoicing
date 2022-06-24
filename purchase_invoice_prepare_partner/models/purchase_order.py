from odoo import models
import logging
_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        if self.partner_invoice_id:
            res["partner_invoice_id"] = self.partner_invoice_id.id
        if self.partner_id:
            res["partner_id"] = self.partner_id.id
        return res
