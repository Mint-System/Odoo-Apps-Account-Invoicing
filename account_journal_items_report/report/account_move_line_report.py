from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class AccountMoveLineReport(models.Model):
    _name = 'account.move.line.report'
    _description = 'Journal items grouped by account'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)

        # Group by account

        # Calculated cumulated balance

        return {
            'doc_ids': docids,
            'doc_model': 'account.move.line',
            'docs': docs,
        }