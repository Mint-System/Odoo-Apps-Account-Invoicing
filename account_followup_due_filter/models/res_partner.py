import logging

from odoo import fields, models
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_unreconciled_aml_domain(self):
        """Updates domain in the same way as _compute_total_due."""
        unreconciled_aml_domain = super()._get_unreconciled_aml_domain()
        today = fields.Date.context_today(self)
        overdue_unreconciled_aml_domain = expression.AND(
            [
                unreconciled_aml_domain,
                [
                    "|",
                    "&",
                    ("date_maturity", "!=", False),
                    ("date_maturity", "<", today),
                    "&",
                    ("date_maturity", "=", False),
                    ("date", "<", today),
                ],
            ]
        )
        return overdue_unreconciled_aml_domain
