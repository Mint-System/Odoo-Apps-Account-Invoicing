import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    reconcile_date = fields.Date(compute="_compute_get_reconcile_date", store=True)

    @api.depends("payment_state")
    def _compute_get_reconcile_date(self):
        for move in self:
            move_lines = self.env["account.move.line"].browse(
                move.line_ids._reconciled_lines()
            )
            if move_lines:
                move.reconcile_date = max(move_lines.mapped("date"))
