{
    "name": "Account Move Line Position",
    "summary": """
        Enable line position number and link from purchase or sale order.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Accounting",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["sale_order_line_position", "purchase_order_line_position"],
    "data": ["views/account_move.xml", "views/res_config_settings.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
