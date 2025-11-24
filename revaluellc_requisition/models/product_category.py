# -*- coding: utf-8 -*-
""" Product Category """
from odoo import api, fields, models, _


class ProductCategory(models.Model):
    """ inherit Product Category """
    _inherit = 'product.category'

    set_budget = fields.Boolean()
    requisition_budget = fields.Float()