# -*-coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class ResUsers(models.Model):
    _inherit = 'res.users'

    direction=fields.Many2one('atm.direction' , string="Direction :")
    fonction = fields.Many2one('atm.fonction' , String="Fonction :")
