# -*- coding: utf-8 -*-
{
    'name': "NG2i POS",

    'summary': """
        Point de vente : améliorations 
        """,

    'description': """
        -- ajout sortie stock sur premier emplacement du produit
    """,

    'author': "NG2i",
    'website': "https://ng2i.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/19.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '19.0.0.6',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    # always loaded
    'data': [
        'data/pos_data.xml',
        'views/stockMove.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            'ng2i_pos/static/src/**/*',
        ],
    },

    # only loaded in demonstration mode
    'demo': [
    ],
}
