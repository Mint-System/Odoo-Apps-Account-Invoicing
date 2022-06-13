{
    "name": "Account Move Line Accounting Description Stock",
    "summary": """
        Copy stock move description to external name on invoice creation.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Invoicing",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "account_move_line_accounting_description",
        "stock_picking_invoice_link",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
