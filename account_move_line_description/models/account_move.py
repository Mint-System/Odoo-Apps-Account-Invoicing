import logging

from odoo import models

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_computed_name(self):
        if self.partner_id.lang:
            product = self.product_id.with_context(lang=self.partner_id.lang)
        else:
            product = self.product_id

        # Return product name without reference if not other description is given
        if not product.description_sale and not product.description_purchase:
            return self.product_id.name

        return super()._get_computed_name()
