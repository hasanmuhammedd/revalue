# -*- coding: utf-8 -*-
""" Stock Picking """
from odoo import api, fields, models, _


class StockPicking(models.Model):
    """ inherit Stock Picking """
    _inherit = 'stock.picking'

    requisition_order_id = fields.Many2one('purchase.requisition.order',
                                           string="Requisition")
    project = fields.Char()
    purchase_requisition_order_ids = fields.One2many(
        'purchase.requisition.order', 'picking_id')

    count_requisition = fields.Integer(compute='_compute_count_requisition', store=True)

    @api.depends('purchase_requisition_order_ids')
    def _compute_count_requisition(self):
        """ Compute count_requisition value """
        for rec in self:
            rec.count_requisition = len(rec.purchase_requisition_order_ids.ids)

    def action_view_all_purchase_requisition(self):
        self.ensure_one()

        result = {
            "type": "ir.actions.act_window",
            "res_model": "purchase.requisition.order",
            "domain": [('picking_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Requisition."),
            'view_mode': 'list,form',
        }
        return result

    def requisition_order(self):
        """ Transfer """
        items = []
        for rec in self.move_ids_without_package:
            items.append((0, 0, {
                'product_id': rec.product_id.id,
                'description': rec.description_picking,
                'quantity': rec.product_uom_qty,
                'project': rec.project,
                'uom_id': rec.product_uom.id,
                'demand': rec.product_uom_qty,
            }))

        action = \
            self.env.ref(
                'revaluellc_requisition.picking_material_requisition_action').sudo().read()[
                0]
        action['context'] = {
            'default_picking_material_requisition_line_ids': items,
        }
        action['views'] = [
            (self.env.ref(
                'revaluellc_requisition.picking_material_requisition_form').id,
             'form')]
        return action


class StockMove(models.Model):
    """ inherit Stock Move """
    _inherit = 'stock.move'

    project = fields.Char()

    def open_on_hand(self):
        """ Utility method used to add an "Open Parent" button in partner views """
        self.ensure_one()
        address_form_id = self.env.ref(
            'stock.view_stock_quant_tree_inventory_editable').id
        return {'type': 'ir.actions.act_window',
                'res_model': 'stock.quant',
                'context': {'create': 0, 'edit': 0,'hide_set_button':True},
                'domain': [('product_id', '=', self.product_id.id),
                           ('on_hand', '=', True),('show_on_hand', '=', True)],
                'view_mode': 'form',
                'views': [(address_form_id, 'list')],
                'target': 'new',
                }

    def _prepare_procurement_values(self):
        """
        Allows to transmit analytic account from moves to new
        moves through procurement.
        """
        res = super()._prepare_procurement_values()
        if self.analytic_distribution:
            res.update(
                {
                    "project": self.project
                }
            )
        return res

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        """
        We fill in the analytic account when creating the move line from
        the move
        """
        res = super()._prepare_move_line_vals(
            quantity=quantity, reserved_quant=reserved_quant
        )

        res.update({"project": self.project})
        return res


class StockMoveLine(models.Model):
    """ inherit Stock Move Line """
    _inherit = 'stock.move.line'

    project = fields.Char(related='move_id.project')
    mac_address = fields.Char()

    @api.model
    def _prepare_stock_move_vals(self):
        """
        In the case move lines are created manually, we should fill in the
        new move created here with the analytic account if filled in.
        """
        res = super()._prepare_stock_move_vals()
        if self.analytic_distribution:
            res.update({"project": self.project})
        return res

    def _prepare_new_lot_vals(self):
        self.ensure_one()
        return {
            'name': self.lot_name,
            'product_id': self.product_id.id,
            'company_id': self.company_id.id,
            'mac_address': self.mac_address
        }
