from . import controllers

import odoo
from odoo.tools import config


def pre_init_hook(cr):
    server_wide_modules = config.get('server_wide_modules') or ''
    server_wide_modules = server_wide_modules.split(',')
    if 'og_database_comment' not in server_wide_modules:
        try:
            server_wide_modules.append('og_database_comment')
            config['server_wide_modules'] = ','.join(server_wide_modules)
            config.save()
            odoo.modules.module.load_openerp_module('og_database_comment')
        except:
            pass
        