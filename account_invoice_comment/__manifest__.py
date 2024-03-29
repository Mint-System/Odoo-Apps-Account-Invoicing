{
    "name": "Account Invoice Comment",
    "summary": """
        Comment field in invoice.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Accounting",
    "version": "16.0.1.1.0",
    "license": "AGPL-3",
    "depends": ["account", "sale"],
    "data": ["views/account.xml", "views/res_config_settings_views.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
