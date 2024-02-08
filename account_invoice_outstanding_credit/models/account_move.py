import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    has_outstanding_move_lines = fields.Boolean(
        default=False, compute="_compute_has_outstanding_move_lines", store=True
    )

    @api.depends("partner_id", "state", "payment_state")
    def _compute_has_outstanding_move_lines(self):
        for move in self:
            domain = [
                ("partner_id", "=", move.partner_id.id),
                ("move_type", "=", "out_refund"),
                ("parent_state", "=", "posted"),
                ("account_id.reconcile", "=", True),
                ("amount_residual", "!=", 0),
            ]
            outstanding_move_lines = self.env["account.move.line"].search_count(domain)
            move.has_outstanding_move_lines = (
                True if outstanding_move_lines > 0 else False
            )

    def action_post(self):
        res = super().action_post()
        for move in self.filtered(lambda m: m.move_type == "out_refund"):
            domain = [
                ("partner_id", "=", move.partner_id.id),
                ("payment_state", "!=", "paid")
            ]
            outstanding_moves = self.env["account.move"].search(domain)
            outstanding_moves._compute_has_outstanding_move_lines()
