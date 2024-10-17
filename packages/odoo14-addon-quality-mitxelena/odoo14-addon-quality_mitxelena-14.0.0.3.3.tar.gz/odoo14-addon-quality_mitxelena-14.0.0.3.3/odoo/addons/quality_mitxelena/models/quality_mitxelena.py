from odoo import api, fields, models, exceptions, _ # type: ignore

import requests
import logging
import base64

from logging import getLogger
_logger = getLogger(__name__)
class Product(models.Model):
    _inherit = ["product.template"]
    product_test = fields.Many2one(comodel_name='qc.test', string='Test', tracking=True)
    test_question = fields.One2many(related='product_test.test_lines')

    
class Question(models.Model):
    _inherit = ["qc.test.question"]

    sequence = fields.Integer(string="Sequence", required=True, default="1")
    valor_nominal = fields.Float(string='Valor Nominal', store=True)
    cota_min = fields.Float(string='Cota Mínima', digits="Quality Control")
    cota_max = fields.Float(string='Cota Máxima', digits="Quality Control")
    min_value = fields.Float(string="Min", digits="Quality Control", compute="_compute_test", store=True)    
    max_value = fields.Float(string="Max", digits="Quality Control", compute="_compute_test", store=True)
    short_notes = fields.Text(string='Notes', store=True, compute='_compute_short_notes')
    icon_select= fields.Selection(selection=[('paralelismo.png', 'Paralelismo'),
                                            ('simetria.png', 'Simetria'),
                                            ('inclinacion.png', 'Inclinacion'),
                                            ('redondez.png', 'Redondez'),
                                            ('planicidad.png', 'Planicidad'),
                                            ('posicion.png', 'Posicion'),
                                            ('perpendicularidad.png', 'Perpendicularidad'),
                                            ('formasuperficie.png', 'Forma Superficie'),
                                            ('circular.png', 'Circular'),
                                            ('total.png', 'Total'),
                                            ('cilindricidad.png', 'Cilindricidad'),
                                            ('formalinea.png', 'Forma Linea'),
                                            ('concentricidad.png', 'Concentricidad'),
                                            ('rectitud.png', 'Rectitud')
                                            ], string='Icon Select', tracking=True)
    icon = fields.Binary(string='Icon', store=True, compute='_compute_icon', attachment=False)
        
    def get_uom_mm(self):        
        uoms = self.env['uom.uom'].search([('name', '=', 'mm')])
        return uoms[0].id if uoms.exists() else False
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', store=True, default=get_uom_mm)

    def default_name(self):
        for record in self:
            record.name = str(record.sequence) + '# '
    name = fields.Char(string='Name', required=True, tracking=True, default=default_name)    

    @api.onchange('name', 'sequence')
    def _onchange_name(self):
        for record in self:
            if record.name:
                pos = record.name.find('# ')
                if pos != -1:
                    record.name = record.name[pos + 2:]
                record.name = str(record.sequence) + '# ' + str(record.name)
            else:
                record.name = str(record.sequence) + '# '

    @api.depends("icon_select")
    def _compute_icon(self):
        for record in self:
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
            if record.icon_select:
                url = base_url + '/quality_mitxelena/static/src/img/' + record.icon_select
                icon = ""
                try:    
                    icon = base64.b64encode(requests.get(url.strip()).content).replace(b"\n", b"")
                except Exception as e:
                    _logger.warning("Can't load the image from URL %s" % url)
                    logging.exception(e)                
                record.update({"icon": icon, })
    
    @api.depends('notes', 'short_notes')
    def _compute_short_notes(self):
        for record in self:
            if record.notes:
                record.short_notes = record.notes[:30] + '...' if len(record.notes) > 30 else record.notes

    @api.depends('valor_nominal', 'cota_min', 'cota_max')
    def _compute_test(self):        
        for record in self:
            record.min_value = record.valor_nominal + record.cota_min            
            record.max_value = record.valor_nominal + record.cota_max
            
            
    @api.constrains("cota_min", "cota_max")
    def _check_cota_valid_range(self):
        for record in self:
            if record.type == "quantitative" and record.cota_min > record.cota_max:
                raise exceptions.ValidationError(
                    _(
                        "Question '%s' is not valid: "
                        "minimum value can't be higher than maximum value."
                    )
                    % record.name_get()[0][1]
                )