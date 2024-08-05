from odoo import models, api

class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _custom_reconcile_invoices(self):
        pass

        for move in self.filtered(lambda m: m.payment_state == "not_paid"):
            payment = self.env["account.payment"].search(
                [("ref", "=", move.payment_reference)], limit=1
            )
            if payment:
                move_line = move.line_ids.filtered(
                    lambda l: l.name == move.payment_reference
                )[0]
                payment
