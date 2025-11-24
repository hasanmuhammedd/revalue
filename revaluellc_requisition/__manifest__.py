# -*- coding: utf-8 -*-
{
    'name': "revaluellc_requisition",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '18.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'uom', 'stock', 'purchase', 'purchase_requisition','sale','revaluellc_stock_picking_check_validate'],

    # always loaded
    'data': [
        'security/requisition_groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/requisition_order.xml',
        'views/product_category.xml',
        'views/stock_picking.xml',
        'views/purchase_order.xml',
        'views/purchase_agreements.xml',
        # 'views/stock_quant.xml',
        'views/res_partner.xml',
        'views/material_request.xml',
        'views/product_template.xml',
        'views/stock_lot.xml',
        # 'views/sale_order.xml',
        'views/stock_location.xml',
        'wizard/transfer_requisition_order.xml',
        'wizard/consolidate_material_request.xml',
        'wizard/picking_material_requisition.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
