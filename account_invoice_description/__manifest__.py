{
    'name': "Account Invoice Description",

    'summary': """
        Add description to invoice form and report.
    """,

    'author': "Mint System GmbH, Odoo Community Association (OCA)",
    'website': "https://www.mint-system.ch",
    'category': 'Accounting',
    'version': '14.0.1.0.1',
    'license': 'AGPL-3',

    'depends': ['account'],

    'data': [
        'views/report_invoice_document.xml',
        'views/view_move_form.xml',
    ],

    'installable': True,
    'application': False,
    "images": ["images/screen.png"],
}