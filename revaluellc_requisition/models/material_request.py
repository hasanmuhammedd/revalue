# -*- coding: utf-8 -*-
""" Material Request """
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MaterialRequest(models.Model):
    """ Material Request """
    _name = 'material.request'
    _description = 'Material Request'

    product_id = fields.Many2one('product.product')
    demand = fields.Float()
    project = fields.Char()
    delivery_time = fields.Date()
    delivery = fields.Char()
    requested = fields.Float()
    remaining = fields.Float(compute='_compute_remaining', store=True)
    state = fields.Selection([('draft', 'Draft'),('full_cons', 'Full Cons'),('part_cons', 'Part Cons')],default='draft',compute='_compute_state')

    def _compute_state(self):
        """ Compute state value """
        for rec in self:
            if rec.remaining>0 and  rec.remaining < rec.demand:
                rec.state = 'part_cons'
            elif rec.remaining == 0:
                rec.state = 'full_cons'
            elif rec.remaining == rec.demand:
                rec.state = 'draft'

    @api.depends('demand','requested')
    def _compute_remaining(self):
        """ Compute remaining value """
        for rec in self:
            rec.remaining = rec.demand - rec.requested

    def consolidate(self):
        """ consolidate """

        items = []
        for rec in self:

            items.append((0, 0, {
                'project': rec.project,
                'product_id': rec.product_id.id,
                'demand': rec.remaining,
                'material_request_id': rec.id,

                                 }))

        if items:
            action = \
                self.env.ref(
                    'revaluellc_requisition.consolidate_material_request_action').sudo().read()[
                    0]
            action['context'] = {

                'default_consolidate_material_request_line_ids': items,

            }
            action['views'] = [
                (self.env.ref(
                    'revaluellc_requisition.consolidate_material_request_form').id,
                 'form')]
            return action
        else:
            raise ValidationError(
                _("Not Record Selected"))
    