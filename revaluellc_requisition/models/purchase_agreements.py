# -*- coding: utf-8 -*-
""" Purchase Requisition """
from odoo import api, fields, models, _

class PurchaseRequisition(models.Model):
    """ inherit Purchase Requisition """
    _inherit = 'purchase.requisition'

    purchase_requisition_id = fields.Many2one('purchase.requisition.order')

class PurchaseRequisitionLine(models.Model):
    """ inherit Purchase Requisition Line """
    _inherit = 'purchase.requisition.line'

    project = fields.Char()

    def _prepare_purchase_order_line(self, name, product_qty=0.0, price_unit=0.0, taxes_ids=False):
        res = super(PurchaseRequisitionLine, self)._prepare_purchase_order_line(name, product_qty, price_unit, taxes_ids)
        res['project'] = self.project
        return res