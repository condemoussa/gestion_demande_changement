# -*-coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class AtmAnn(models.Model):
    _name = "atm.ann"
    _rec_name = "annee_en_cours"

    libelle = fields.Char(string='Nom')
    annee_en_cours = fields.Integer(string="Année en cours", compute='_compute_annee_en_cours', store=True)

    @api.depends('libelle')
    def _compute_annee_en_cours(self):
        for record in self:
            current_year = fields.Date.context_today(self).year
            record.annee_en_cours = current_year




