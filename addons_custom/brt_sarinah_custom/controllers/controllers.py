# -*- coding: utf-8 -*-
# from odoo import http


# class BrtSarinahCustom(http.Controller):
#     @http.route('/brt_sarinah_custom/brt_sarinah_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/brt_sarinah_custom/brt_sarinah_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('brt_sarinah_custom.listing', {
#             'root': '/brt_sarinah_custom/brt_sarinah_custom',
#             'objects': http.request.env['brt_sarinah_custom.brt_sarinah_custom'].search([]),
#         })

#     @http.route('/brt_sarinah_custom/brt_sarinah_custom/objects/<model("brt_sarinah_custom.brt_sarinah_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('brt_sarinah_custom.object', {
#             'object': obj
#         })
