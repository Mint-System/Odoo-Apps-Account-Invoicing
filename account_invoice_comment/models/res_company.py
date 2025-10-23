import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = "res.company"

    copy_sale_order_comment = fields.Boolean()
