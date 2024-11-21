# -*- coding: utf-8 -*-

from odoo import models, fields, api


class informacion(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'ejemplo de odoo básico'

    name = fields.Char(required=True,size=20,string="Título")
    descripcion = fields.Text(string="La descripción")
    alto_en_cms = fields.Integer(string="Alto en cms:")
    ancho_en_cms = fields.Integer(string="Ancho en cms:")
    largo_en_cms = fields.Integer(string="Largo en cms:")
    peso = fields.Float(digits=(6,2),default=2.7,string="Peso en KGs:")
    autorizado = fields.Boolean(string="¿Autorizado?", default=True)
    sexo_traducido = fields.Selection([('Hombre','Home'),('Mujer','Muller'),('Otros','Outros')],string="Sexo:")
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

