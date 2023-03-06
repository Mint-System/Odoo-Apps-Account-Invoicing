from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    client_order_ref = fields.Text()