# -*-coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from datetime import datetime

class DemandeChange(models.Model):
    _name = "demande.change"
    _description = "Demande de changement"
    _inherit = "mail.thread"
    _rename = 'name'

    def imprimer_demande(self):
        dt=""
        dt1 = ""
        dt2 = ""
        dt3= ""
        dt4 = ""
        dt5 = ""
        dt6 = ""
        dt7 = ""
        dt8 = ""
        dt9 = ""
        selected_rows = self.env['demande.change'].browse(self.env.context.get('active_ids', []))
        for row in selected_rows:
            if row.dat_cochang:
                dt=row.dat_cochang.strftime('%d/%m/%Y')
            if row.dat_debut:
                dt1=row.dat_debut.strftime('%d/%m/%Y')
            if row.dat_fin:
                dt2=row.dat_fin.strftime('%d/%m/%Y')
            if row.dat_affect:
                dt3=row.dat_affect.strftime('%d/%m/%Y')
            if row.dat_traitemnt:
                dt4=row.dat_traitemnt.strftime('%d/%m/%Y')
            if row.dat_accept:
                dt5=row.dat_accept.strftime('%d/%m/%Y')
            if row.dat_refus:
                dt6=row.dat_refus.strftime('%d/%m/%Y')
            if row.dat_recep_change:
                dt7=row.dat_recep_change.strftime('%d/%m/%Y')
            if row.dat_trait_change:
                dt8 = row.dat_trait_change.strftime('%d/%m/%Y')
            if row.dat_accept_approb:
                dt9 = row.dat_accept_approb.strftime('%d/%m/%Y')
            demande = self.env['demande.change'].search_read([("name", "=", row.name)])

            data = { "resultat": demande ,

                     "dat1":dt ,
                     "dat_debut":dt1,
                      "dat_fin" :dt2,
                      "dat_reception":dt3,
                      "dat_traitement":dt4,
                      "dat_accept":dt5,
                      "dat_refus": dt6,
                      "dat_reception_cha": dt7,
                      "dat_traitement_cha":dt8,
                      "dat_app": dt9,
                     }

            return self.env.ref('gestion_demande_changement.action_rapport_demande_changement_pdf').with_context(
                    landscape=True).report_action(self, data=data)


    @api.model
    def create(self, vals):
        last_years = self.env["atm.anneee"].search([], order='id desc', limit=1)
        record = super(DemandeChange, self).create(vals)
        if record:
            record['name'] = "CH-" + str(last_years.annee_en_cours) +"-"+"000"+ str(record.chrono_ann)
        return record

    @api.constrains("dat_debut", "dat_fin")
    def _check_date_range(self):
        for line in self:
            if line.dat_debut and line.dat_fin:
                if line.dat_debut > line.dat_fin:
                    raise models.ValidationError(
                        "la date debut ne peut pas etre postérieure à la date de fin ")

    def soumission(self):
        comite_decision=self.env["res.users"].search([("type_users","=","comite_decision")])
        for line in comite_decision:
            # last_demande = self.env["demande.change"].search([], order='id desc', limit=1)
            subject = "Demande de changement"
            body = f"Cher(e) {line.name},\n\nVous avez une nouvelle demande de changement de la part de {self.demandeur_name.name}."

            self.env['mail.mail'].create({
                'subject': subject,
                'body_html': body,
                'email_from': 'mconde@iwc-ci.com',
                'email_to': line.login,
                'email_cc': 'condemoussa05@gmail.com',
                'state': 'outgoing'
            }).send()
        self.write({"state":"submit"})


    def validation(self):
        chef_projet = self.env["res.users"].search([("type_users", "=", "chef_projet")])
        for line in chef_projet:
            subject = "Validation de la demande"
            body = f"Cher(e) {line.name},\n\nVotre demande a été validée par le comité de décision."

            self.env['mail.mail'].create({
                'subject': subject,
                'body_html': body,
                'email_from': 'mconde@iwc-ci.com',
                'email_to': self.destin_name.login,
                'email_cc': line.login,
                'state': 'outgoing'
            }).send()

        self.write({"state":"valided"})



    def annuler(self):
        chef_projet = self.env["res.users"].search([("type_users", "=", "chef_projet")])
        for line in chef_projet:
            subject = "Annulation de la demande"
            body = f"Cher(e) {line.name},\n\nVotre demande a été annulée par le comité de décision."

            self.env['mail.mail'].create({
                'subject': subject,
                'body_html': body,
                'email_from': 'mconde@iwc-ci.com',
                'email_to': line.login,
                'email_cc': 'condemoussa05@gmail.com',
                'state': 'outgoing'
            }).send()

        self.write({"state": "submit"})

    @staticmethod
    def _truncate_text(text, max_chars=30):
        # Fonction pour tronquer le texte à un nombre maximal de caractères
        if isinstance(text, str) and len(text) > max_chars:
            return text[:max_chars] + '...'
        return text

    @api.depends('descri_change')
    def _compute_short_description(self):
        for record in self:
            record.descri_change_short = self._truncate_text(record.descri_change)
            record.analyse_impact_short = self._truncate_text(record.analyse_impact)
            record.risque_short = self._truncate_text(record.risque)
            record.pla_act_ret_short = self._truncate_text(record.pla_act_ret)
            record.obser_bloquant_short = self._truncate_text(record.obser_bloquant)
            record.obser_non_bloquant_short = self._truncate_text(record.obser_non_bloquant)
            record.visa_membre_short = self._truncate_text(record.visa_membre)
            record.obser_comi_change_short = self._truncate_text(record.obser_comi_change)
            record.visa_membre_approb_short = self._truncate_text(record.visa_membre_approb)
            record.comm_refu_short = self._truncate_text(record.comm_refu)




    #partie du chef de projet
    name = fields.Char(" Numero d'ordre :",readonly=True)
    motif_change=fields.Selection([
        ("projet","Projet"),
        ("modification_majeure", " Modification Majeure"),
    ],default="projet" ,string="Motif :",required=True,tracking=True)
    numero_ysi=fields.Char("4-Fiche Easyvista (DI /DS..) N°.... :")
    perim_concern = fields.Char("Périmetre concerné :")
    demandeur_name = fields.Many2one("res.users",string="Nom et prénom(s) : ")
    name_dem=fields.Char("Nom et prénom(s) :" ,related="demandeur_name.name")
    demandeur_visa = fields.Binary("Visa demandeur :")
    demandeur_name_chef = fields.Many2one("res.users", string="Nom et prénom(s) :")
    nom_chef_dem = fields.Char(string="Nom et prénom(s) :" ,related="demandeur_name_chef.name")
    demandeur_visa_chef = fields.Binary("Visa demandeur :")
    descri_change=fields.Text("DESCRIPTION :")
    descri_change_short = fields.Text(string='Description', compute='_compute_short_description', store=True)
    destin_name = fields.Many2one("res.users", string="Nom et prénom(s) :")
    nom_destin=fields.Char( string="Nom et prénom(s) :" , related="destin_name.name")
    destin_fonct = fields.Char("Fonction :")
    dat_debut = fields.Date("Date debut :")
    dat_fin = fields.Date("Date fin :")
    #2- LISTES DES DOCUMENTS JOINTS
    ordre_deploi = fields.Boolean(default=True,string="1-Ordre de deploiement")
    opt2 = fields.Boolean(default=True,string="2-Check-list des actions du deploiement")
    opt3 = fields.Boolean(default=True,string="3-Accord DGA domaine ou responsable MOA (Mail ou CR réunion")
    opt4 = fields.Boolean(default=True ,string=" 4-Fiche Easyvista (DI,DS..) N°..")
    opt5 = fields.Boolean(default=True,string="5-Rapport ou planning de formation utilisateur")
    opt6 = fields.Boolean(default=True,string="6-Rapport de tests")
    opt7 = fields.Boolean(default=True,string="7-Document d'installation et de confiuration")
    opt8 = fields.Boolean(default=True,string="8-Document d'exploitation")
    opt9 = fields.Boolean(default=True, string="9-Entrée EZV")
    opt10 = fields.Boolean(default=True, string="10-Accord du CVATL")
    opt11 = fields.Boolean(default=True, string="11-Fiche d'evaluation PRI")
    opt12 = fields.Boolean(default=True, string="12-Fiche de Supervision de l'application")
    opt13 = fields.Boolean(default=True, string="13-Planification des traitements dans l'ORDONNANCEUR")
    opt14 = fields.Boolean(default=True, string="14-Rapport RSE")
    opt15 = fields.Boolean(default=True, string="15-Propriété intellectuelle :.....")
    opt16 = fields.Boolean(default=True, string="16-Preuve d'existence ou pas d'un certificat")
    opt17 = fields.Boolean(default=True, string="18-Autres (A preciser)...........")
    opt18 = fields.Boolean(default=True, string="17-Fiche de Sauvegarde de l'application")
    ##4- RISQUES ET PLAN D'ACTION DE RETOUR ARRIERE
    analyse_impact = fields.Text("Analyse de l'impact du changement :",nolabel=True)
    analyse_impact_short=fields.Text(string="Analyse de l'impact du changement ", compute='_compute_short_description', store=True)
    risque = fields.Text("Risques : ")
    risque_short=fields.Text(string="Risques ", compute='_compute_short_description', store=True)
    #5- DECISION DU COMITE DE GESTION DES CHANGEMENTS
    pla_act_ret = fields.Text(" Plan d'action de retour arriere :")
    pla_act_ret_short=fields.Text(string="Plan d'action de retour arriere ", compute='_compute_short_description', store=True)
    gestionnaire_name = fields.Many2one("res.users", string="Nom et prénom(s) : ")
    nom_gestion=fields.Char(string="Nom et prénom(s) : " ,related="gestionnaire_name.name")
    dat_affect = fields.Date(" Date de reception :")
    dat_traitemnt = fields.Date("Date traitement :")
    state=fields.Selection([
        ("draft","Brouillon"),
        ("submit", "Soumise"),
        ("valided","Validée"),
        ("cancel","Annulée")
    ],default="draft")
    anne_id=fields.Many2one("atm.anneee","Année en cours :",default=lambda self: self._default_anne_id(),readonly=True)
    chrono_ann=fields.Integer("Chrono",compute="_compute_count_chrono",store=True)
    dat_cochang=fields.Date("Date Cochange :" )


    # partie du comite de decision
    obser_bloquant=fields.Text("Observations bloquantes  :")
    obser_bloquant_short=fields.Text(string="Observations bloquantes ", compute='_compute_short_description', store=True)

    obser_non_bloquant = fields.Text("Observations non bloquantes  :")
    obser_non_bloquant_short=fields.Text(string="Observations non  bloquantes ", compute='_compute_short_description', store=True)
    visa_membre=fields.Text()
    visa_membre_short=fields.Text(compute='_compute_short_description', store=True)
    decision_accor=fields.Boolean("Accord :")
    decision_refus = fields.Boolean("Refus :")
    n_chrone=fields.Integer("N°chrono :")
    dat_accept=fields.Date("Date :")
    nom_presi_seance=fields.Many2one("res.users",string="President de seance :")
    no_presi_sean=fields.Char(string="President de seance :" , related="nom_presi_seance.name")
    dat_refus = fields.Date("Date :")
    comm_refu=fields.Text("Commentaire :")
    comm_refu_short=fields.Text(string="Commentaire ", compute='_compute_short_description', store=True)
    president_change=fields.Many2one("res.users",string="Nom et prénom(s) :")
    no_presi_chan=fields.Char(string="Nom et prénom(s):" ,related="president_change.name")
    dat_trait_change=fields.Date("Date de reception :")
    dat_recep_change = fields.Date("Date de traitement :")
    obser_comi_change=fields.Text()
    obser_comi_change_short=fields.Text(compute='_compute_short_description', store=True)
    visa_membre_approb = fields.Text()
    visa_membre_approb_short=fields.Text(compute='_compute_short_description', store=True)
    decision_fin=fields.Selection([("accord","Accord"),("refus","Refus")],string="Decision :")
    n_chrone_approb = fields.Integer("N°chrono :")
    dat_accept_approb = fields.Date("Date: ")
    nom_presi_seance_approb= fields.Many2one("res.users", string="President de seance :")
    no_presi_sean_apro=fields.Char(string="President de seance :" ,related="nom_presi_seance_approb.name")

    @api.depends('motif_change')
    def _compute_count_chrono(self):
        last_years = self.env["atm.anneee"].search([], order='id desc', limit=1)
        for record in self:
            count = self.env['demande.change'].search_count(
                [('anne_id', '=', last_years.id)])
            record.chrono_ann = count

    def _default_anne_id(self):
        last_years = self.env["atm.anneee"].search([], order='id desc', limit=1)
        default_annee = self.env['atm.anneee'].search([('id', '=',last_years.id)], limit=1)
        return default_annee

    def write(self, vals):
        for line in self:
            if line.state == "valided":
                raise models.UserError("Désolé, vous ne pouvez plus modifier cet enregistrement. Merci !")
        return super(DemandeChange, self).write(vals)




