# -*- coding: utf-8 -*-
""" Transfer Requisition Order """
from odoo import api, fields, models, _


class TransferRequisitionOrder(models.TransientModel):
    """ Transfer Requisition Order """
    _name = 'transfer.requisition.order'
    _description = 'Transfer Requisition Order'

    picking_type_id = fields.Many2one(
        'stock.picking.type',
        domain="[('code','=','internal')]"
    )
    location_id = fields.Many2one(
        'stock.location', string='Source Location'
    )
    location_dest_id = fields.Many2one(
        'stock.location', string='Destination Location'
    )
    transfer_requisition_order_line_ids = fields.One2many(
        'transfer.requisition.order.line', 'transfer_requisition_order_id')

    transfer_type = fields.Selection(
        [('transfer', 'Transfer'), ('purchase', 'Purchase')])
    requisition_type = fields.Selection(
        [('tender', 'Tender'), ('purchase', 'Purchase'),
         ('material_request', 'Material Request')], default="tender")
    partner_id = fields.Many2one('res.partner', string="Vendor")
    project = fields.Char()

    @api.onchange('picking_type_id')
    def _onchange_stock_picking_default_location(self):
        """ stock_picking_id """
        for rec in self:
            if rec.picking_type_id:
                rec.location_id = rec.picking_type_id.default_location_src_id.id
                rec.location_dest_id = rec.picking_type_id.default_location_dest_id.id

    def confirm(self):
        """ Confirm """
        active_id = self._context.get('active_id')
        requisition = self.env['purchase.requisition.order'].browse(
            active_id)
        items = []
        if self.transfer_type == 'transfer':
            for rec in self.transfer_requisition_order_line_ids:
                items.append((0, 0,
                              {'product_id': rec.product_id.id,
                               'name': rec.name,
                               'location_id': self.location_id.id,
                               'location_dest_id': self.location_dest_id.id,
                               'product_uom_qty': rec.quantity}))
            self.env['stock.picking'].sudo().create(
                {'picking_type_id': self.picking_type_id.id,
                 'location_id': self.location_id.id,
                 'location_dest_id': self.location_dest_id.id,
                 'requisition_order_id': requisition.id,
                 'move_ids_without_package': items})
        elif self.transfer_type == 'purchase':
            if self.requisition_type == 'tender':
                for rec in self.transfer_requisition_order_line_ids:
                    items.append((0, 0,
                                  {'product_id': rec.product_id.id,
                                   'product_uom_id': rec.uom_id.id,
                                   'product_qty': rec.quantity}))

                    self.env['purchase.requisition'].create({
                        'purchase_requisition_id': requisition.id,
                        'line_ids': items

                    })


            elif self.requisition_type == 'purchase':
                for rec in self.transfer_requisition_order_line_ids:
                    items.append((0, 0,
                                  {'product_id': rec.product_id.id,
                                   'product_uom': rec.uom_id.id,
                                   'product_qty': rec.quantity}))

                    self.env['purchase.order'].create({
                        'partner_id': self.partner_id.id,
                        'purchase_requisition_id': requisition.id,
                        'order_line': items

                    })
            elif self.requisition_type == 'material_request':
                for rec in self.transfer_requisition_order_line_ids:
                    self.env['material.request'].create({
                        'product_id': rec.product_id.id,
                        'demand': rec.quantity,
                        'project': self.project

                    })


class TransferRequisitionOrderLine(models.TransientModel):
    """ Transfer Requisition Order Line """
    _name = 'transfer.requisition.order.line'
    _description = 'Transfer Requisition Order Line'

    transfer_requisition_order_id = fields.Many2one(
        'transfer.requisition.order')
    product_id = fields.Many2one('product.product')
    name = fields.Text(string="Description")
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure',
                             related='product_id.uom_id')
    quantity = fields.Float()
