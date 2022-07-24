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
    'category': 'Sales',
    'version': '0.1',
    'application': True,
    # any module necessary for this one to work correctly, depends itu pake nama modules
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/perpustakaan.xml',
        'views/inherit_product_view.xml',
        'views/list_buku.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
