import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    has_outstanding_credits = fields.Boolean(
        default=False, compute="_compute_has_outstanding_credits", store=True
    )

    @api.model
    def not_paid_invoices_from_partner(self, partner_id):
        domain = [
            ("commercial_partner_id", "=", partner_id.id),
            ("move_type", "=", "out_invoice"),
            ("payment_state", "not in", ["paid", "reversed"]),
        ]
        invoices = self.env["account.move"].search(domain)
        return invoices

    def has_unreconciled_credit_move_lines(self):
        domain = [
            ("partner_id", "=", self.commercial_partner_id.id),
            ("move_type", "=", "out_refund"),
            ("parent_state", "=", "posted"),
            ("account_id.reconcile", "=", True),
            ("amount_residual", "!=", 0),
        ]
        credit_move_lines = self.env["account.move.line"].search_count(domain)
        return credit_move_lines > 0

    @api.depends("payment_state")
    def _compute_has_outstanding_credits(self):
        """
        When an outgoing invoice is updated compute the oustanding credits field.
        """
        for move in self:
            if move.has_unreconciled_credit_move_lines() and move.payment_state not in [
                "paid",
                "reversed",
            ]:
                move.has_outstanding_credits = True
            else:
                move.has_outstanding_credits = False

    def action_post(self):
        res = super().action_post()
        for move in self.filtered(lambda m: m.move_type == "out_refund"):
            self.not_paid_invoices_from_partner(
                move.commercial_partner_id
            )._compute_has_outstanding_credits()
        return res

    def button_draft(self):
        res = super().button_draft()
        for move in self.filtered(lambda m: m.move_type == "out_refund"):
            self.not_paid_invoices_from_partner(
                move.commercial_partner_id
            )._compute_has_outstanding_credits()
        return res

    def button_cancel(self):
        res = super().button_cancel()
        for move in self.filtered(lambda m: m.move_type == "out_refund"):
            self.not_paid_invoices_from_partner(
                move.commercial_partner_id
            )._compute_has_outstanding_credits()
        return res


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def reconcile(self):
        res = super().reconcile()
        for line in self:
            self.env["account.move"].not_paid_invoices_from_partner(
                line.partner_id
            )._compute_has_outstanding_credits()
        return res
