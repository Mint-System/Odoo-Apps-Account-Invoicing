from odoo import models, fields


class BankRecWidget(models.Model):
    _inherit = "bank.rec.widget"

    def _action_trigger_matching_rules(self):
        # Extend the existing method to implement custom logic
        matching = super()._action_trigger_matching_rules()

        # Custom matching logic
        if not matching or not matching.get("aml_ids"):
            # If no match found, try custom reconciliation logic
            candidate_move_lines = self._find_matching_move_lines()

            if candidate_move_lines:
                self.matched_move_lines = candidate_move_lines
                self.matched_partner_id = (
                    candidate_move_lines[0].partner_id.id
                    if candidate_move_lines[0].partner_id
                    else None
                )
                matching = {
                    "aml_ids": candidate_move_lines.ids,
                    "status": "reconciled",
                    "auto_reconcile": True,
                }

        return matching

    def _find_matching_move_lines(self):
        """Find move lines that match based on payment reference and amount."""
        self.ensure_one()

        # Search for move lines with matching payment reference and amount
        domain = [
            ("move_id.state", "=", "posted"),
            ("amount_residual", "=", self.amount),
            ("payment_reference", "=", self.payment_reference),
            ("company_id", "=", self.company_id.id),
        ]

        move_lines = self.env["account.move.line"].search(domain)

        return move_lines
