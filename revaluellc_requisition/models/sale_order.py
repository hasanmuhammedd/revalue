# -*- coding: utf-8 -*-
""" Sale Order """
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    """ inherit Sale Order """
    _inherit = 'sale.order'

    project = fields.Char()
    project_name = fields.Char()

