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

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # Added new field for our to set default discount payment term and will
    # be adding when partner selected from account move object if value found
    discount_payment_term_id = fields.Many2one(
        "account.payment.term",
        string="Vendor Discount Term",
        help="Default payment term used for this supplier.",
    )
