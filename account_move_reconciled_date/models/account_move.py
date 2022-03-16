from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    reconcile_date = fields.Date(compute='_compute_get_reconcile_date')

    def _compute_get_reconcile_date(self):
        for move in self:
            reconcilation_dates = []
            # Get reconciliation infos
            for partial, amount, counterpart_line in move._get_reconciled_invoices_partials():
                # Get all lines from payment move
                for line in counterpart_line.move_id.line_ids:
                    # Get reconcilation lines where bank statement is give
                    reconcile_lines = self.env['account.move.line'].browse(line._reconciled_lines()).filtered(lambda l: l.statement_id)
                    reconcilation_dates.extend(reconcile_lines.mapped('date'))
            
            move.reconcile_date = max(reconcilation_dates) if reconcilation_dates else None