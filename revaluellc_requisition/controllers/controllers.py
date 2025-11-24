# -*- coding: utf-8 -*-
# from odoo import http


# class RevaluellcRequisition(http.Controller):
#     @http.route('/revaluellc_requisition/revaluellc_requisition', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/revaluellc_requisition/revaluellc_requisition/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('revaluellc_requisition.listing', {
#             'root': '/revaluellc_requisition/revaluellc_requisition',
#             'objects': http.request.env['revaluellc_requisition.revaluellc_requisition'].search([]),
#         })

#     @http.route('/revaluellc_requisition/revaluellc_requisition/objects/<model("revaluellc_requisition.revaluellc_requisition"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('revaluellc_requisition.object', {
#             'object': obj
#         })
