import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    invoice_cash_rounding_id = fields.Many2one(
        "account.cash.rounding",
        string="Default Cash Rounding Method",
        related="company_id.invoice_cash_rounding_id",
        readonly=False,
    )
