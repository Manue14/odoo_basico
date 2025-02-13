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
    # Os campos Many2one crean un campo na BD
    moneda_id = fields.Many2one('res.currency', domain="[('position','=','after')]")
    moneda_en_texto = fields.Char(related="moneda_id.currency_unit_label",
                                 string="Moneda en formato texto")
    creador_da_moneda = fields.Char(related="moneda_id.create_uid.login",
                                   string="Usuario creador da moneda", store=True)
    moneda_euro_id = fields.Many2one('res.currency',
                                    default=lambda self: self.env['res.currency'].search([('name', '=', "EUR")],
                                                                                         limit=1))
    gasto_en_euros = fields.Monetary("Gasto en Euros", 'moneda_euro_id')
    moneda_dolar_id = fields.Many2one('res.currency',
                                     default=lambda self: self.env['res.currency'].search([('name', '=', "USD")],
                                                                                          limit=1))
    gasto_en_dolares = fields.Monetary("Gasto en Dólares", 'moneda_dolar_id')

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

    def _cambia_campo_sexo(self, rexistro):
        rexistro.sexo_traducido = "Hombre"

    def envio_email(self):
        meu_usuario = self.env.user
        #mail_de     Odoo pon o email que configuramos en gmail para facer o envio
        mail_reply_to = meu_usuario.partner_id.email  # o enderezo email que ten asociado o noso usuario
        mail_para = 'micifu14@gmail.com'  # o enderezo email de destino
        mail_valores = {
            'subject': 'Aquí iría o asunto do email ',
            'author_id': meu_usuario.id,
            'email_from': mail_reply_to,
            'email_to': mail_para,
            'message_type': 'email',
            'body_html': 'Aquí iría o corpo do email cos datos por exemplo de "%s" ' % self.descripcion,
        }
        mail_id = self.env['mail.mail'].create(mail_valores)
        mail_id.sudo().send()
        return True