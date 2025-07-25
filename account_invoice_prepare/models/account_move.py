from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    print_date = fields.Datetime()

    def action_print_pdf(self):
        res = super().action_print_pdf()
        if res:
            self.print_date = fields.Datetime.now()
        return res

    def action_prepare_pdf(self):
        invoices_report = self.env.ref("account.account_invoices")
        for invoice in self:
            content, _content_type = self.env["ir.actions.report"]._render_qweb_pdf(
                invoices_report, res_ids=[invoice.id]
            )
            invoice.print_date = fields.Datetime.now()
