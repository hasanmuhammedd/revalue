# -*- coding: utf-8 -*-
""" Picking Material Requisition """
from odoo import api, fields, models, _


class PickingMaterialRequisition(models.TransientModel):
    """ Picking Material Requisition """
    _name = 'picking.material.requisition'
    _description = 'Picking Material Requisition'

    picking_material_requisition_line_ids = fields.One2many(
        'picking.material.requisition.line', 'picking_material_requisition_id')

    def confirm(self):
        """ Confirm """
        active_id = self._context.get('active_id')
        picking = self.env['stock.picking'].browse(
            active_id)
        items = []
        for rec in self.picking_material_requisition_line_ids:
            if rec.select:
                items.append((0, 0, {
                    'product_id': rec.product_id.id,
                    'name': rec.description,
                    'quantity': rec.quantity,
                    'uom_id': rec.uom_id.id,
                }))
        self.env['purchase.requisition.order'].sudo().create(
            {'picking_id': picking.id,
             'project':picking.project,
             'requisition_order_line_ids': items })


class PickingMaterialRequisitionLine(models.TransientModel):
    """ Picking Material Requisition Line """
    _name = 'picking.material.requisition.line'
    _description = 'Picking Material Requisition Line'

    picking_material_requisition_id = fields.Many2one(
        'picking.material.requisition')

    product_id = fields.Many2one('product.product')
    project = fields.Char()
    description = fields.Text()
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure')
    demand = fields.Float()
    quantity = fields.Float()
    select = fields.Boolean()
