# -*- coding: utf-8 -*-
{
    'name': "Training Day 2",

    'summary': """Odoo Training""",

    'description': """
        Training module for managing trainings:
            - training courses
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/training.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
