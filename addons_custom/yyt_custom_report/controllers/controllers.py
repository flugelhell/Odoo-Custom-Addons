# -*- coding: utf-8 -*-
# from odoo import http


# class YytCustomReport(http.Controller):
#     @http.route('/yyt_custom_report/yyt_custom_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/yyt_custom_report/yyt_custom_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('yyt_custom_report.listing', {
#             'root': '/yyt_custom_report/yyt_custom_report',
#             'objects': http.request.env['yyt_custom_report.yyt_custom_report'].search([]),
#         })

#     @http.route('/yyt_custom_report/yyt_custom_report/objects/<model("yyt_custom_report.yyt_custom_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('yyt_custom_report.object', {
#             'object': obj
#         })
