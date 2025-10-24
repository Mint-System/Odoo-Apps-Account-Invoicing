{
    "name": "Sale Invoice Cash Rounding Default",
    "summary": """
        Apply default cash rounding when invoicing sale orders.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Sale",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["account", "sale"],
    "data": ["views/res_config_settings_views.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
