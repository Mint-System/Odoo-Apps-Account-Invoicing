import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    get_positions_from_orders = fields.Boolean(
        config_parameter="account.get_positions_from_orders"
    )
