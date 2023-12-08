import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    copy_sale_order_comment = fields.Boolean(
        related="company_id.copy_sale_order_comment",
        string="Copy Sale Order Comment",
        readonly=False,
    )
