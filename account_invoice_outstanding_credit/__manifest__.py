{
    "name": "Account Invoice Outstanding Credit",
    "summary": """
        Filter customer invoices with open credits.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Invoicing",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["account"],
    "data": ["views/account_move.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
