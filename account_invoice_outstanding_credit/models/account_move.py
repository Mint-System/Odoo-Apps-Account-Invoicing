import logging

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    has_outstanding_credits = fields.Boolean(default=False)

    def action_post(self):
        """
        When a credit move is posted update the outstanding credits field on related invoices.
        """
        res = super().action_post()
        for move in self.filtered(lambda m: m.move_type == "out_refund"):

            # Get open invoices from the same partner
            domain = [
                ("partner_id", "=", move.partner_id.id),
                ("payment_state", "!=", "paid"),
            ]
            related_invoices = self.env["account.move"].search(domain)

            # Update related invoices
            related_invoices.has_outstanding_credits = True
        return res


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends(
        "debit",
        "credit",
        "amount_currency",
        "account_id",
        "currency_id",
        "company_id",
        "matched_debit_ids",
        "matched_credit_ids",
    )
    def _compute_amount_residual(self):
        super()._compute_amount_residual(self)
        self._update_has_outstanding_credits()

    def _update_has_outstanding_credits(self):
        """
        When a line of a credit move is reconciled update the outstanding credits field on related invoices.
        """
        for line in self.filtered(lambda m: m.move_type == "out_refund"):

            # Get open invoices from the same partner
            domain = [
                ("partner_id", "=", move.partner_id.id),
                ("payment_state", "!=", "paid"),
            ]
            related_invoices = self.env["account.move"].search(domain)

            # Get unreconciled credit lines from the same partner
            domain = [
                ("partner_id", "=", move.partner_id.id),
                ("move_type", "=", "out_refund"),
                ("parent_state", "=", "posted"),
                ("account_id.reconcile", "=", True),
                ("amount_residual", "!=", 0),
            ]
            credit_move_lines = self.env["account.move.line"].search_count(domain)
            has_outstanding_credits = True if credit_move_lines > 0 else False

            # Update related invoices
            related_invoices.write({"has_outstanding_credits": has_outstanding_credits})
