# -*- coding: utf-8 -*-
""" Product Template """
from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    """ inherit Product Template """
    _inherit = 'product.template'

    tracking_by_mac = fields.Boolean()