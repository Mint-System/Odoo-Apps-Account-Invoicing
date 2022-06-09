from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        if self.comment:
            invoice_vals["comment"] = self.comment
        return invoice_vals
