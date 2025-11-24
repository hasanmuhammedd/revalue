# -*- coding: utf-8 -*-
""" Res Partner """
from odoo import api, fields, models, _


class ResPartner(models.Model):
    """ inherit Res Partner """
    _inherit = 'res.partner'

    is_vendor = fields.Boolean()
    vendor_type = fields.Selection([('local', 'Local'), ('foreign', 'Foreign')])
