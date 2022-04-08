##############################################################################
#
# Nivels GmbH
# Comercialstrasse 19
# 7000 Chur
#
# Copyright (C) 2022 Nivels GmbH.
# All Rights Reserved
#
##############################################################################

from odoo import api, models, fields, _
from datetime import timedelta, datetime


class AccountMove(models.Model):
    _inherit = 'account.move.line'

    has_discount = fields.Boolean('Discount', default=False)


class AccountMove(models.Model):
    _inherit = 'account.move'

    discount_payment_term_id = fields.Many2one('account.payment.term',
                                               string='Vendor Discount Term',
                                               help='Assigned supplier payment term used for discount calculation.')
    has_discount = fields.Boolean(string='Supplier Discount',
                                  help='True if the vendor has can be used for discount')
    discount_date = fields.Date('Discount Date')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        super()._onchange_partner_id()
        for rec in self:
            if rec.partner_id.discount_payment_term_id:
                rec.discount_payment_term_id = rec.partner_id.discount_payment_term_id.id

    def action_update_discount(self):
        for rec in self.filtered(lambda x: x.discount_payment_term_id and x.state not in ('posted', 'cancel')):
            discount_line = rec.discount_payment_term_id.line_ids.filtered(
                lambda x: x.value == 'discount' and x.discount_product).sorted(key=lambda x: x.days, reverse=False)
            context = {'default_move_type': self._context.get('default_move_type'), 'journal_id': rec.journal_id,
                       'default_partner_id': rec.commercial_partner_id,
                       'default_currency_id': rec.currency_id or rec.company_currency_id}
            invoice_line = rec.invoice_line_ids.filtered(lambda x: x.has_discount)
            if rec.invoice_date and discount_line:
                for discount in discount_line:
                    discount_date = rec.invoice_date + timedelta(discount.days)
                    if discount_date > datetime.today().date():
                        rec.with_context(context).write({
                            'has_discount': True,
                            'discount_date': discount_date,
                            'invoice_line_ids': [(2, invoice_line.id), (0, 0, {
                                'name': discount.discount_product.name,
                                'product_id': discount.discount_product.id,
                                'tax_ids': [(6, 0, discount.discount_product.supplier_taxes_id.ids)],
                                'move_id': rec.id,
                                'account_id': rec.journal_id.default_account_id.id,
                                'quantity': 1,
                                'has_discount': True,
                                'price_unit': -(sum(rec.invoice_line_ids.filtered(lambda x: not x.has_discount).mapped(
                                    'price_subtotal')) * (1 - (discount.value_amount / 100))),
                            })]
                        })
                        break
                else:
                    if invoice_line:
                        rec.with_context(context).write({
                            'has_discount': False,
                            'discount_date': False,
                            'invoice_line_ids': [(2, invoice_line.id)],
                        })
            else:
                if invoice_line:
                    rec.with_context(context).write({
                        'has_discount': False,
                        'discount_date': False,
                        'invoice_line_ids': [(2, invoice_line.id)],
                    })

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(AccountMove, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if toolbar and result.get('toolbar') and self._context.get('default_move_type') != 'in_invoice':
            for action in result['toolbar']['action']:
                if action['name'] == 'Update Discount' and action['type']== 'ir.actions.server':
                    result['toolbar']['action'].remove(action)
        return result
