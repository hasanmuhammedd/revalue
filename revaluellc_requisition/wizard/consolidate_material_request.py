# -*- coding: utf-8 -*-
""" Consolidate Material Request """
from odoo import api, fields, models, _


class ConsolidateMaterialRequest(models.TransientModel):
    """ Consolidate Material Request """
    _name = 'consolidate.material.request'
    _description = 'Consolidate Material Request'

    partner_id = fields.Many2one('res.partner', string="Vendor")
    consolidate_material_request_line_ids = fields.One2many(
        'consolidate.material.request.line', 'consolidate_material_request_id')

    def confirm(self):
        """ Confirm """
        items=[]
        for rec in self.consolidate_material_request_line_ids:
            items.append((0, 0,
                          {'product_id': rec.product_id.id,
                           'product_uom_id': rec.uom_id.id,
                           'project':rec.project,
                           'product_qty': rec.request}))
            rec.material_request_id.requested+=rec.request

        self.env['purchase.requisition'].create({
            'vendor_id': self.partner_id.id,
            'line_ids': items

        })

class ConsolidateMaterialRequestLine(models.TransientModel):
    """ Consolidate Material Request Line """
    _name = 'consolidate.material.request.line'
    _description = 'Consolidate Material Request Line'

    consolidate_material_request_id = fields.Many2one(
        'consolidate.material.request')
    project = fields.Char()
    product_id = fields.Many2one('product.product')
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure',related='product_id.uom_id')
    demand = fields.Float()
    request = fields.Float()
    remaining = fields.Float(compute='_compute_remaining', store=True)
    material_request_id = fields.Many2one('material.request')

    @api.depends('demand','request')
    def _compute_remaining(self):
        """ Compute remaining value """
        for rec in self:
            rec.remaining = rec.demand- rec.request


