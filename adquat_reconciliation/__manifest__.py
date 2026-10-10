# -*- coding: utf-8 -*-
{
    'name': "Adquat Reconciliation",

    'summary': """
        Comptabilité : rapprochement bancaire ordre tri""",

    'description': """
        Comptabilité : rapprochement bancaire : tri par ordre décroissant
    """,

    'author': "Adquat",
    'website': "http://www.adquat.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Invoicing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account',  ],

    # always loaded
    'data': [
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
