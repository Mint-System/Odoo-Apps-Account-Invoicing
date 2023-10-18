from odoo import api, models


class ReportSwissQR(models.AbstractModel):
    _inherit = "report.l10n_ch.qr_report_main"

    @api.model
    def _get_report_values(self, docids, data=None):
        res = super()._get_report_values(docids, data)
        docs = self.env["account.move"].browse(docids)
        for invoice in docs:
            res[invoice.id] = invoice.partner_bank_id.build_qr_code_base64(
                invoice.amount_residual,
                invoice.name,
                invoice.payment_reference,
                invoice.currency_id,
                invoice.partner_id,
                qr_method="ch_qr",
                silent_errors=False,
            )
        return res
