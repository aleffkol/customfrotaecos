# -*- coding: utf-8 -*-
{
    'name': "Custom Frota",

    'summary': """
        Neste módulo estará sendo apresentando um sistema de frotas
        de maneira customizada, diferente do sistema de frota nativo.""",

    'description': """
        Desenvolvimento do sistema de frota customizada.
    """,

    'author': "Ecos PB (Aleff Kluivert;Antônio Neto)",
    'website': "https://ecospb.org/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Frota',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/carro.xml',
        'views/frota.xml',
        'views/contrato.xml',
        'views/frota_sequence.xml',
        'views/contrato_sequence.xml',
        'views/condutor.xml',
        'views/gastos.xml',
        'views/gastos_sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
