from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    carrier_id = fields.Many2one('delivery.carrier', string="Delivery Method", domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", help="Fill this field if you plan to invoice the shipping based on picking.")

    @api.onchange('partner_id')
    def _onchange_carrier_id(self):
        for move in self.filtered(lambda m: not m.carrier_id):
            move.carrier_id = move.partner_id.property_delivery_carrier_id