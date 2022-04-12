import logging
from odoo import _, api, fields, models, exceptions
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.constrains("ref", "payment_reference")
    def _check_bank_type_for_type_isr(self):
        """OVERWRITE: Do not raise exception on missing isr subscription"""
        for move in self:
            if move.move_type == "out_invoice" and move._has_isr_ref():
                bank_acc = move.partner_bank_id
                if not bank_acc:
                    raise exceptions.ValidationError(
                        _(
                            "Bank account shouldn't be empty, for ISR ref"
                            " type, you can set it manually or set appropriate"
                            " payment mode."
                        )
                    )
        return True