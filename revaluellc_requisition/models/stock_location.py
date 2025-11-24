# -*- coding: utf-8 -*-
""" Stock Location """
from odoo import api, fields, models, _


class StockLocation(models.Model):
    """ inherit Stock Location """
    _inherit = 'stock.location'


    show_on_hand = fields.Boolean()
