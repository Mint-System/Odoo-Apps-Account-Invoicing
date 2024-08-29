import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    reconcile_date = fields.Date(compute="_compute_get_reconcile_date", store=True)

    @api.depends("payment_state")
    def _compute_get_reconcile_date(self):
        for move in self:
            reconciliation_dates = []
            # _logger.warning(f"Starting computation of reconcile_date for move ID: {move.id}")

            # Get reconciliation infos
            for partial_info in move._get_reconciled_invoices_partials():
                if len(partial_info) < 3:
                    # _logger.warning(f"Unexpected tuple length: {len(partial_info)} in partial info: {partial_info}")
                    continue

                # Ensure counterpart_line is correctly identified
                partial, amount, counterpart_line = partial_info

                # Check if counterpart_line is a recordset
                if not isinstance(counterpart_line, models.BaseModel):
                    # _logger.warning(f"Expected counterpart_line to be a recordset, got {type(counterpart_line)}. Full tuple: {partial_info}")
                    continue

                # _logger.warning(f"Processing counterpart_line ID: {counterpart_line.id} for move ID: {move.id}")

                try:
                    # Get all lines from payment move
                    for line in counterpart_line.move_id.line_ids:
                        # _logger.warning(f"Processing line ID: {line.id} in move ID: {move.id}")
                        # Get reconciliation lines where a bank statement is given
                        reconcile_lines = (
                            self.env["account.move.line"]
                            .browse(line._reconciled_lines())
                            .filtered(lambda l: l.statement_id)
                        )
                        # _logger.warning(f"Found {len(reconcile_lines)} reconciliation lines with statements for line ID: {line.id}")
                        reconciliation_dates.extend(reconcile_lines.mapped("date"))
                except AttributeError:
                    # _logger.error(f"Error processing counterpart_line ID: {counterpart_line.id} in move ID: {move.id}: {str(e)}")
                    continue

            # Set the reconcile date to the latest reconciliation date, if available
            move.reconcile_date = (
                max(reconciliation_dates) if reconciliation_dates else None
            )
            # _logger.warning(f"Set reconcile_date for move ID: {move.id} to {move.reconcile_date}")
