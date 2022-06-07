from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_sale_id = fields.Many2one('res.partner', string="Sale Contact Address")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        res= super()._onchange_partner_id()
        addr = self.partner_id.address_get(['sale'])
        values = {
            'partner_sale_id': addr['sale'],
        }
        self.update(values)
        return res