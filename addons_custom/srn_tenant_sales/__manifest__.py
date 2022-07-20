# -*- coding: utf-8 -*-
{
    'name': "Sarinah Tenant Sales",

    'summary': """Input Sales of Sarinah Tenant""",

    'description': """
        Input Sales of Sarinah Tenant
    """,

    'author': "Yayat",
    'website': "https://sarinah.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/tenant_sales.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
