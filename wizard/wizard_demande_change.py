# -*- coding: utf-8 -*-

from odoo import fields, models ,api


class DemandePrintChange(models.TransientModel):
    _name = "demande.change.report"
    _description = "Demande de changement"

    numero_demande= fields.Char('N° demande')
    numero_de=fields.Many2one("demande.change" ,string="N° Demande ")



    def test(self):
        selected_rows = self.env['demande.change'].browse(self.env.context.get('active_ids', []))
        for row in selected_rows:
            data = {'form_data': self.read()[0], }
            demande = self.env['demande.change'].search_read([("name", "=", row.name)])
            nb_demande = len(demande)
            if self.numero_de and nb_demande != 0:
                data = {'form_data': self.read()[0],
                        "resultat": demande
                        }

                return self.env.ref('gestion_demande_changement.action_rapport_demande_changement_pdf').with_context(
                    landscape=True).report_action(self, data=data)
            else:
                raise models.UserError("Desolé , vous devez obligatoirement saisir un numero correct  d'une demande.")


