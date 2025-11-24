# -*- coding: utf-8 -*-
""" Requisition Order """
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PurchaseRequisitionOrder(models.Model):
    """ Purchase Requisition Order """
    _name = 'purchase.requisition.order'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Purchase Requisition Order'

    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'),
                              ('send_to_pm_approve', 'Send To PM Approve'),
                              ('pm_approved', 'PM Approved'),
                              ('pm_rejected', 'PM Rejected'), ('lock', 'Lock')],
                             default='draft', string='Status')
    name = fields.Char(default="New")
    description = fields.Html()
    date = fields.Date(default=fields.Date.today())
    requisition_order_line_ids = fields.One2many('requisition.order.line',
                                                 'purchase_requisition_order_id')
    requisition_category_budget_ids = fields.One2many(
        'requisition.category.budget', 'purchase_requisition_order_id')
    show_category_budget = fields.Boolean()
    stock_picking_ids = fields.One2many('stock.picking', 'requisition_order_id')
    count_picking = fields.Integer(compute='_compute_count_picking', store=True)
    purchase_order_ids = fields.One2many('purchase.order',
                                         'purchase_requisition_id')
    count_purchase_order = fields.Integer(
        compute='_compute_count_purchase_order', store=True)
    purchase_requisition_ids = fields.One2many('purchase.requisition',
                                               'purchase_requisition_id')
    count_purchase_requisition = fields.Integer(
        compute='_compute_count_purchase_requisition', store=True)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    project = fields.Char()
    project_id = fields.Many2one('project.project')
    picking_id = fields.Many2one('stock.picking')


    show_select_all = fields.Boolean(compute="_compute_show_buttons", store=False)
    show_deselect_all = fields.Boolean(compute="_compute_show_buttons", store=False)

    @api.depends("requisition_order_line_ids", "requisition_order_line_ids.select")
    def _compute_show_buttons(self):
        for rec in self:
            lines = rec.requisition_order_line_ids
            if not lines or len(lines) <= 1:
                rec.show_select_all = False
                rec.show_deselect_all = False
            else:
                selected = lines.filtered(lambda l: l.select)
                if len(selected) == len(lines):
                    rec.show_select_all = False
                    rec.show_deselect_all = True
                elif not selected:
                    rec.show_select_all = True
                    rec.show_deselect_all = False
                else:
                    rec.show_select_all = True
                    rec.show_deselect_all = True

    def select_all(self):
        """ Select All """
        for rec in self:
            if rec.requisition_order_line_ids:
                for rec2 in rec.requisition_order_line_ids:
                    rec2.select = True

    def deselect_all(self):
        """ Select All """
        for rec in self:
            if rec.requisition_order_line_ids:
                for rec2 in rec.requisition_order_line_ids:
                    rec2.select = False

    @api.depends('purchase_requisition_ids')
    def _compute_count_purchase_requisition(self):
        """ Compute count_picking value """
        for rec in self:
            rec.count_purchase_requisition = len(
                rec.purchase_requisition_ids.ids)

    def action_view_all_purchase_requisition(self):
        self.ensure_one()

        result = {
            "type": "ir.actions.act_window",
            "res_model": "purchase.requisition",
            "domain": [('purchase_requisition_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Purchase Agreements"),
            'view_mode': 'list,form',
        }
        return result

    @api.depends('purchase_order_ids')
    def _compute_count_purchase_order(self):
        """ Compute count_picking value """
        for rec in self:
            rec.count_purchase_order = len(rec.purchase_order_ids.ids)

    def action_view_all_purchase_order(self):
        self.ensure_one()

        result = {
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "domain": [('purchase_requisition_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Purchase Order"),
            'view_mode': 'list,form',
        }
        return result

    @api.depends('stock_picking_ids')
    def _compute_count_picking(self):
        """ Compute count_picking value """
        for rec in self:
            rec.count_picking = len(rec.stock_picking_ids.ids)

    def action_view_all_stock_picking(self):
        self.ensure_one()

        result = {
            "type": "ir.actions.act_window",
            "res_model": "stock.picking",
            "domain": [('requisition_order_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Stock Picking"),
            'view_mode': 'list,form',
        }
        return result

    def transfer(self):
        """ Transfer """
        items = []
        for rec in self.requisition_order_line_ids:
            if rec.select:
                items.append((0, 0, {'product_id': rec.product_id.id,
                                     'name': rec.name,
                                     'quantity': rec.quantity}))
                rec.select = False
        if items:
            action = \
                self.env.ref(
                    'revaluellc_requisition.transfer_requisition_order_action').sudo().read()[
                    0]
            action['context'] = {
                'default_transfer_requisition_order_line_ids': items,
                'default_transfer_type': 'transfer'
            }
            action['views'] = [
                (self.env.ref(
                    'revaluellc_requisition.transfer_requisition_order_form').id,
                 'form')]
            return action
        else:
            raise ValidationError(
                _("Not Record Selected"))

    def purchase(self):
        """ Purchase """

        items = []
        for rec in self.requisition_order_line_ids:
            if rec.select:
                items.append((0, 0, {'product_id': rec.product_id.id,

                                     'name': rec.name,
                                     'quantity': rec.quantity}))
                rec.select = False
        if items:
            action = \
                self.env.ref(
                    'revaluellc_requisition.transfer_requisition_order_action').sudo().read()[
                    0]
            action['context'] = {
                'default_transfer_requisition_order_line_ids': items,
                'default_transfer_type': 'purchase',
                'default_project': self.project,
            }
            action['views'] = [
                (self.env.ref(
                    'revaluellc_requisition.transfer_requisition_order_form').id,
                 'form')]
            return action
        else:
            raise ValidationError(
                _("Not Record Selected"))

    def lock_order(self):
        """ Lock """
        for rec in self:
            rec.state = 'lock'

    def pm_rejected(self):
        """ Pm Rejected """
        for rec in self:
            rec.state = 'pm_rejected'

    def pm_approved(self):
        """ Pm Approved """
        for rec in self:
            rec.state = 'pm_approved'

    def send_to_pm_approve(self):
        """ Send To Pm Approve """
        for rec in self:
            rec.state = 'send_to_pm_approve'
            rec.show_category_budget = True

    def confirm(self):
        """ Confirm """
        for rec in self:
            items = []
            t = []
            t2 = []
            for b in rec.requisition_order_line_ids:
                total_cost = 0
                for r in rec.requisition_order_line_ids:
                    if b.product_id.categ_id.id == r.product_id.categ_id.id and b.product_id.categ_id.id not in t:
                        total_cost += r.product_id.standard_price * r.quantity
                t.append(b.product_id.categ_id.id)
                if b.product_id.categ_id.id not in t2:
                    if b.product_id.categ_id.set_budget:
                        requisition_budget = str(
                            b.product_id.categ_id.requisition_budget)
                    else:
                        requisition_budget = "not limit budget"
                    items.append((0, 0, {
                        'product_category_id': b.product_id.categ_id.id,
                        'budget_of_category': requisition_budget,
                        'total_cost': total_cost}))
                    t2.append(b.product_id.categ_id.id)
            rec.write({'requisition_category_budget_ids': items})
            rec.state = 'confirmed'

    @api.model
    def create(self, vals):
        """ Override create method to sequence name """
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'purchase.requisition.order') or '/'
        return super(PurchaseRequisitionOrder, self).create(vals)


class RequisitionOrderLine(models.Model):
    """ Requisition Order Line """
    _name = 'requisition.order.line'
    _description = 'Requisition Order Line'

    purchase_requisition_order_id = fields.Many2one(
        'purchase.requisition.order', invisible=True)
    product_id = fields.Many2one('product.product')
    name = fields.Text(string="Description")
    uom_id = fields.Many2one('uom.uom', string='Unit Of Measure',
                             related='product_id.uom_id')
    quantity = fields.Float()
    select = fields.Boolean()

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """ product_id """
        for rec in self:
            rec.name = rec.product_id.name

    def open_on_hand(self):
        """ Utility method used to add an "Open Parent" button in partner views """
        self.ensure_one()
        address_form_id = self.env.ref(
            'stock.view_stock_quant_tree_inventory_editable').id
        return {'type': 'ir.actions.act_window',
                'res_model': 'stock.quant',
                'context': {'create': 0, 'edit': 0, 'hide_set_button': True},
                'domain': [('product_id', '=', self.product_id.id),
                           ('on_hand', '=', True)],
                'view_mode': 'form',
                'views': [(address_form_id, 'list')],
                'target': 'new',
                }


class RequisitionCategoryBudget(models.Model):
    """ Requisition Category Budget """
    _name = 'requisition.category.budget'
    _description = 'Requisition Category Budget'

    purchase_requisition_order_id = fields.Many2one(
        'purchase.requisition.order')
    product_category_id = fields.Many2one('product.category')
    total_cost = fields.Float()
    budget_of_category = fields.Char()
