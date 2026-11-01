# -*- coding: utf-8 -*-
{
    'name': "NG2i Report",

    'summary': """
        Impressions : en-tête, pied de page, factures et devis du Vieux Pressoir
        """,

    'description': """
        -- reprise des personnalisations d'impression de la base v14
    """,

    'author': "NG2i",
    'website': "https://ng2i.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/19.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '19.0.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['account', 'sale'],

    # always loaded
    'data': [
        'views/report_templates.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
    ],
}
