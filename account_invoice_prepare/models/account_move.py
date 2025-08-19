import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


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
            filename = "%s.pdf" % (invoice._get_report_base_filename().replace("/", "_"))
            existing_invoice = self.env["ir.attachment"].search(
                [("res_id", "=", invoice.id), ("res_model", "=", "account.move"), ("name", "=", filename)]
            )
            _logger.warning([filename, existing_invoice])
            existing_invoice.unlink()
            content, _content_type = self.env["ir.actions.report"]._render_qweb_pdf(
                invoices_report, res_ids=[invoice.id]
            )
            invoice.print_date = fields.Datetime.now()
