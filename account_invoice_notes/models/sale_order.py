from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        if self.note_header:
            invoice_vals["note_header"] = self.note_header
        if self.note_footer:
            invoice_vals["note_footer"] = self.note_footer
        return invoice_vals
