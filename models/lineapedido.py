from odoo import models, fields, api
from odoo.exceptions import ValidationError

class lineapedido(models.Model):
    _name = 'odoo_basico.lineapedido'
    _description = 'linea de un pedido en odoo básico'
    _sql_constraints = [('nombreUnico', 'unique(name)', 'No se puede repetir el nombre')]

    pedido_id = fields.Many2one('odoo_basico.pedido',
                                ondelete="cascade", required=True)
    informacion_ids = fields.Many2many("odoo_basico.informacion",
                                       string="Rexistro de Información",
                                       relation="odoo_basico_lineapedido_informacion",
                                       column1="lineapedido_id", column2="informacion_id")
    descripcion_lineapedido = fields.Char(required=True, string="Descripción")
    cantidad = fields.Integer(string="Cantidad:")
    num_1 = fields.Integer(string="Número 1:")
    num_2 = fields.Integer(string="Número 1:")
