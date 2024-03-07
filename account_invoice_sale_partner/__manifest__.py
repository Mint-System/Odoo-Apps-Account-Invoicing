{
    "name": "Account Invoice Sale Partner",
    "summary": """
        Set sale order contact on invoice.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Invoicing",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["account", "partner_type_sale"],
    "data": ["views/account.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
