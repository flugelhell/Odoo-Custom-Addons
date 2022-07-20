# -*- coding: utf-8 -*-
{
    'name': "Training",

    'summary': """Odoo Training""",

    'description': """
        Training module for managing trainings:
            - training courses
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base', 'point_of_sale', 'account_accountant',
    ],

    # always loaded
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'report/training_report.xml',
        'views/training.xml',
        'wizard/training_wizard_views.xml',
        'views/action_button.xml',
    ],
    'qweb': ['static/src/view/pos_menu.xml'],
    # only loaded in demonstration mode
    'demo': [
    ],
}

