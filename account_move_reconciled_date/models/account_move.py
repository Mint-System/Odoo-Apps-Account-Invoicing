import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    reconcile_date = fields.Date(compute="_compute_get_reconcile_date", store=True)

    @api.depends("payment_state")
    def _compute_get_reconcile_date(self):
        for move in self:
            reconcilation_dates = []
            # Get reconciliation infos
            partials = move._get_reconciled_invoices_partials()
            for partial_info in partials:
                if len(partial_info) == 3:
                    partial, amount, counterpart_line = partial_info
                    # Get all lines from payment move
                    for line in counterpart_line.move_id.line_ids:
                        # Get reconciliation lines where bank statement is given
                        reconcile_lines = (
                            self.env["account.move.line"]
                            .browse(line._reconciled_lines())
                            .filtered(lambda l: l.statement_id)
                        )
                        reconcilation_dates.extend(reconcile_lines.mapped("date"))

            move.reconcile_date = (
                max(reconcilation_dates) if reconcilation_dates else None
            )
