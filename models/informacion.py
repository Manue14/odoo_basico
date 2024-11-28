# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class informacion(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'ejemplo de odoo básico'
    _sql_constraints = [('nombreUnico', 'unique(name)', 'No se puede repetir el nombre')]
    _order = "descripcion desc"

    name = fields.Char(required=True,size=20,string="Título")
    descripcion = fields.Text(string="La descripción")
    alto_en_cms = fields.Integer(string="Alto en cms:")
    ancho_en_cms = fields.Integer(string="Ancho en cms:")
    largo_en_cms = fields.Integer(string="Largo en cms:")
    peso = fields.Float(digits=(6,2),default=2.7,string="Peso en KGs:")
    autorizado = fields.Boolean(string="¿Autorizado?", default=True)
    sexo_traducido = fields.Selection([('Hombre','Home'),('Mujer','Muller'),('Otros','Outros')],string="Sexo:")
    volumen = fields.Float(digits=(6, 7), compute="_volume", store=True, string="Volume m3")
    densidad = fields.Float(digits=(6, 7), compute="_densidad", store=True, string="Densidad kg/m3")
    literal = fields.Char(store=False)
    foto = fields.Binary(string='Foto')
    adjunto_nombre = fields.Char(string="Nombre Adjunto")
    adjunto = fields.Binary(string="Archivo adjunto")

    @api.depends('alto_en_cms', 'largo_en_cms', 'ancho_en_cms')
    def _volume(self):
        for registro in self:
            registro.volumen = float(registro.alto_en_cms) * float(registro.largo_en_cms) * float(
                registro.ancho_en_cms) / 1000000

    @api.onchange('alto_en_cms')
    def _avisoAlto(self):
        for registro in self:
            if registro.alto_en_cms > 7:
                registro.literal = 'El alto tiene un valor posiblemente excesivo %s es mayor que 7' % registro.alto_en_cms
            else:
                registro.literal = ""

    @api.constrains('peso')  # Ao usar ValidationError temos que importar a libreria ValidationError
    def _constrain_peso(self):  # from odoo.exceptions import ValidationError
        for registro in self:
            if registro.peso < 1 or registro.peso > 4:
                raise ValidationError('El peso de %s tiene que ser entre 1 y 4 ' % registro.name)

    @api.depends('peso', 'volumen')
    def _densidad(self):
        for registro in self:
            if registro.volumen == 0:
                registro.densidad = 0
            else:
                registro.densidad = float(registro.peso) / float(registro.volumen)