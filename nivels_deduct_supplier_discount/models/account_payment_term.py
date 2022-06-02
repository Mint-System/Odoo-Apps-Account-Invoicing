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


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term.line"

    # Added new field for set the default discount product on discount payment term
    discount_product = fields.Many2one(
        "product.product",
        string="Discount Product",
        help="Product to use for the supplier discount in vendor bills.",
        domain="[('type', '=', 'service')]",
    )

    # Added new option discount to kind fo valuation and adding discount product
    value = fields.Selection(
        selection_add=[
            ("discount", "Discount"),
        ],
        ondelete={"discount": "set default"},
        help="Select here the kind of valuation related to this payment terms line.",
    )
