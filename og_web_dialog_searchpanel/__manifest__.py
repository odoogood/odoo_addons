# -*- coding: utf-8 -*-
###############################################################################
#    Copyright (C) 2023-TODAY Odoog (<https://www.odoog.com>)
#    Author: Bin He (vnsoft.he@gmailcom)
#    License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
###############################################################################
{
    'name': "Show Dialog Search Panel",
    'version': '16.0.1.0.0',
    'sequence': 99,
    'summary': "Show Dialog Search Panel",
    'description': """Dialog show SearchPanel for Search More menuitem.""",
    'author': 'VnSoft',
    'maintainer': 'Odoog',
    'support': 'vnsoft.he@gmail.com',
    'website': 'https://www.odoog.com',
    'category': 'setting',
    'depends': ['web'],
    'data': [],
    'demo': [],
    'assets': {
        'web.assets_backend': [
            'og_web_dialog_searchpanel/static/src/js/dialog_searchpanel.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': [],
}
