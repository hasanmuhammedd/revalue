# -*- coding: utf-8 -*-
""" Stock Lot """
from odoo import api, fields, models, _

class StockLot(models.Model):
    """ inherit Stock Lot """
    _inherit = 'stock.lot'

    mac_address = fields.Char()
