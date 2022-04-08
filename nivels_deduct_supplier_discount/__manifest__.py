{
    "name": "Nivels Deduct Supplier Discount",
    "summary": """
        Allow discount deduction on vendor bills.
    """,
    "author": "nivels GmbH, Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Accounting",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["account", "purchase"],
    "data": [
        "data/account_move_data.xml",
        "views/account_payment_term_views.xml",
        "views/partner_view.xml",
        "views/account_move_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
