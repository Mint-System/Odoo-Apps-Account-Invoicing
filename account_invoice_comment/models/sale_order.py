from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        if self.comment and self.env.company_id.group_copy_sale_order_comment:
            invoice_vals["comment"] = self.comment
        return invoice_vals
