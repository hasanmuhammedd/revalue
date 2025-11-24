# -*- coding: utf-8 -*-
""" Stock Quant """
from odoo import api, fields, models, _

class StockQuant(models.Model):
    """ inherit Stock Quant """
    _inherit = 'stock.quant'
    
    hide_set_button = fields.Boolean()
    show_on_hand = fields.Boolean(related='location_id.show_on_hand')