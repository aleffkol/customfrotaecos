# -*- coding: utf-8 -*-
# from odoo import http


# class FrotaEcos(http.Controller):
#     @http.route('/frota_ecos/frota_ecos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/frota_ecos/frota_ecos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('frota_ecos.listing', {
#             'root': '/frota_ecos/frota_ecos',
#             'objects': http.request.env['frota_ecos.frota_ecos'].search([]),
#         })

#     @http.route('/frota_ecos/frota_ecos/objects/<model("frota_ecos.frota_ecos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('frota_ecos.object', {
#             'object': obj
#         })
