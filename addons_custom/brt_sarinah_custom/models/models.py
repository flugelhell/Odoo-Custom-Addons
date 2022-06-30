# -*- coding: utf-8 -*-
# BRATA BAYU S, S.kom -


from odoo import models, fields, api


class brt_sarinah_custom(models.Model):
    _name           = 'brt.sarinah_custom'
    _description    = 'Module Custom Sarinah'

    name            = fields.Char(string="Name")
    chflag          = fields.Char(string="Flag", required="True") 
    chdescription   = fields.Text(string="Description")
    dadate          = fields.Datetime(string="Date")
    iovalid         = fields.Boolean(string="Valid")
    devalue         = fields.Float(string="Value")
    invalue         = fields.Integer(string="In Value")
    choptiona       = fields.Char(string="Option A")
    choptionb       = fields.Char(string="Option B")
    choptionc       = fields.Char(string="Option C")
