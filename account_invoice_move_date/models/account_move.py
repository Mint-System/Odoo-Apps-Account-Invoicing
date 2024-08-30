import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends("invoice_date", "company_id")
    def _compute_date(self):
        """Ensure move date is not overwritten by invoice date."""
        for move in self:
            # Store move date
            move_date = move.date
            super()._compute_date()
            # Reset move date if type is outgoing invoice
            if move_date and move.move_type == "out_invoice":
                move.date = move_date

    def _get_accounting_date(self, invoice_date, has_tax):
        """Return move date as accounting date."""
        res = super()._get_accounting_date(invoice_date, has_tax)
        # Return move date if type is outgoing invoice
        if self.date and self.move_type == "out_invoice":
            return self.date
        return res
