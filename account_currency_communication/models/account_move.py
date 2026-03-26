import logging

from odoo import _, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_invoice_computed_reference(self):
        self.ensure_one()
        if self.journal_id.invoice_reference_type == "none" and self.currency_id.invoice_reference_model == "none":
            return ""
        if self.currency_id.invoice_reference_model:
            ref_function = getattr(
                self,
                f"_get_invoice_reference_{self.currency_id.invoice_reference_model}_{self.currency_id.invoice_reference_type}",
                None,
            )
        else:
            ref_function = getattr(
                self,
                f"_get_invoice_reference_{self.journal_id.invoice_reference_model}_{self.journal_id.invoice_reference_type}",
                None,
            )
        if ref_function is None:
            raise UserError(
                _("The combination of reference model and reference type on the journal or currency is not implemented")
            )
        return ref_function()
