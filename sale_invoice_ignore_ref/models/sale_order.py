import logging

from odoo import models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        data = super()._prepare_invoice()
        data["ref"] = ""
        return data
