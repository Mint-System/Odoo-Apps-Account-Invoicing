{
    "name": "Account Invoice Description",
    "summary": """
        Add description to invoice form and report.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Accounting",
    "version": "15.0.2.0.2",
    "license": "AGPL-3",
    "depends": ["account"],
    "data": ["views/report_invoice_document.xml", "views/account_move.xml"],
    "installable": True,
    "application": False,
    "images": ["images/screen.png"],
}
