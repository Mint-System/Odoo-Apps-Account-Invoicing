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


class ResPartner(models.Model):
    _inherit = "res.partner"

    discount_payment_term_id = fields.Many2one('account.payment.term',
                                               string='Vendor Discount Term',
                                               help='Default payment term used for this supplier.')
