# -*- coding: utf-8 -*-
{
    'name': "Perpustakaan",

    'summary': """Perpustakaan""",

    'description': """
        Training membuat module perpustakaan
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly, depends itu pake nama modules
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/perpustakaan.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}