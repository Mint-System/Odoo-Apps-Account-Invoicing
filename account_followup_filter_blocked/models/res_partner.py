import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    has_blocked_aml = fields.Boolean(
        compute="_compute_has_blocked_aml",
        string="Has blocked account move lines",
        store=True,
    )

    @api.depends("unreconciled_aml_ids.blocked")
    def _compute_has_blocked_aml(self):
        for partner in self:
            partner.has_blocked_aml = any(
                partner.unreconciled_aml_ids.mapped("blocked")
            )
