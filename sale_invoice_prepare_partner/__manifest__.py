{
    "name": "Sale Invoice Prepare Partner",
    "summary": """
        Copy invoice and shipping contacts to invoice.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Invoicing",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["sale_management", "account_move_invoice_partner"],
    "data": ["views/sale_order.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
