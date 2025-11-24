# -*- coding: utf-8 -*-
""" Purchase Order """
from odoo import api, fields, models, _

class PurchaseOrder(models.Model):
    """ inherit Purchase Order """
    _inherit = 'purchase.order'

    purchase_requisition_id = fields.Many2one('purchase.requisition.order')
    
class PurchaseOrderLine(models.Model):
    """ inherit Purchase Order Line """
    _inherit = 'purchase.order.line'
    
    project = fields.Char()

    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        for re in res:
            re['project'] = self.project
        return res

    def _prepare_account_move_line(self, move=False):
        res = super()._prepare_account_move_line(move)
        res.update({'project': self.project})
        return res

    def prepare_stock_move_vals(self, picking, price_unit, product_uom_qty,
                                product_uom):
        """ inherit prepare_stock_move_vals(self, picking, price_unit, product_uom_qty, product_uom)() """
        res = super(PurchaseOrderLine, self).prepare_stock_move_vals(
            picking,
            price_unit,
            product_uom_qty,
            product_uom)
        res.update(project=self.project)
        return res