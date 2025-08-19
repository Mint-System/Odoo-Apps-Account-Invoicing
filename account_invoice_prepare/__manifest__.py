# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Invoice Prepare",
    "summary": """
        Store and load invoice pdf file from attachments.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Invoicing",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["account"],
    "data": ["data/account_report.xml", "data/ir_actions.xml", "views/account_move_views.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
