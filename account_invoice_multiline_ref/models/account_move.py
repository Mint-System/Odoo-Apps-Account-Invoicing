import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    ref = fields.Text()

    def _get_move_display_name(self, show_ref=False):
        out_types = ["out_invoice", "out_refund", "out_receipt"]
        return super()._get_move_display_name(
            show_ref=(self.move_type not in out_types)
        )


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    ref = fields.Text()
