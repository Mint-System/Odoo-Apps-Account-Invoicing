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

{
    "name": "Nivels Sams Deduct Supplier Discount",
    "version": "1.5",
    "author": "nivels GmbH",
    "category": "Accounting/Accounting",
    "summary": "Nivels Sams Deduct Supplier Discount",
    "license": "OPL-1",
    "website": "www.nivels.ch",
    "depends": ["account", "purchase"],
    "data": [
        "data/account_move_data.xml",
        "views/account_payment_term_views.xml",
        "views/partner_view.xml",
        "views/account_move_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
