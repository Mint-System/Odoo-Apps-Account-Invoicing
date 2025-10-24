import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    has_outstanding_credits = fields.Boolean(default=False, compute="_compute_has_outstanding_credits", store=True)

    def has_outstanding_credit_move_lines(self):
        """
        Check if move invoice has outstanding move lines by:
        - Matching the partner
        - Filter receivable accounts
        - Check move lines by posted moves only
        - Ensure credit is given
        - And residual amount is zero
        """
        self.ensure_one()

        # Get ids of receivable accounts and id of default payment account
        receivable_account_ids = self.env["account.account"].search([("account_type", "=", "asset_receivable")])
        domain = [
            ("partner_id", "=", self.commercial_partner_id.id),
            ("account_id", "in", receivable_account_ids.ids),
            ("parent_state", "=", "posted"),
            ("credit", ">", 0),
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
            if move.has_outstanding_credit_move_lines() and move.payment_state not in [
                "paid",
                "reversed",
            ]:
                move.has_outstanding_credits = True
            else:
                move.has_outstanding_credits = False

    @api.model
    def not_paid_invoices_from_partner(self, partner_id):
        domain = [
            ("commercial_partner_id", "=", partner_id.id),
            ("move_type", "=", "out_invoice"),
            ("payment_state", "not in", ["paid", "reversed"]),
        ]
        invoices = self.env["account.move"].search(domain)
        _logger.warning(invoices)
        return invoices

    def action_post(self):
        res = super().action_post()
        for move in self.filtered(lambda m: m.move_type in ["out_refund", "entry"]):
            self.not_paid_invoices_from_partner(move.commercial_partner_id)._compute_has_outstanding_credits()
        return res

    def button_draft(self):
        res = super().button_draft()
        for move in self.filtered(lambda m: m.move_type in ["out_refund", "entry"]):
            self.not_paid_invoices_from_partner(move.commercial_partner_id)._compute_has_outstanding_credits()
        return res

    def button_cancel(self):
        res = super().button_cancel()
        for move in self.filtered(lambda m: m.move_type in ["out_refund", "entry"]):
            self.not_paid_invoices_from_partner(move.commercial_partner_id)._compute_has_outstanding_credits()
        return res


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def reconcile(self):
        res = super().reconcile()
        for line in self:
            self.env["account.move"].not_paid_invoices_from_partner(line.partner_id)._compute_has_outstanding_credits()
        return res
