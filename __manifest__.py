# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (c) 2011 CCI Connect asbl (http://www.cciconnect.be) All Rights Reserved.
#                       Philmer <philmer@cciconnect.be>

{
    'name': 'DEMANDE DE CHANGEMENT',
    'version': '1.0',
    'category': 'Accounting/Accounting',
    'description': """
     ce module permettant de gerer les demande changement
    """,
    'depends': ['base','web','mail'],
    'data': [
            'security/ir.model.access.csv',
            'security/gestion_droit.xml',
            'views/demande_change.xml',
            'wizard/wizard_demande_change.xml',
            'rapport_pdf_demande/template_demande_change.xml',
            'views/menu_generale.xml',
            #'rapport_pdf_demande/report_demande_pdf.xml'
    ],
    'css': [
        'static/src/css/ivoire_status.css',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
