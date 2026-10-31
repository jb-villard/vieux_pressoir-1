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
    # Check https://github.com/odoo/odoo/blob/19.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Invoicing',
    'version': '19.0.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['account_accountant'],

    # always loaded
    'data': [
        'views/bank_rec_widget_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
