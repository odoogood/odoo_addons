from odoo.addons.web.controllers.database import Database as DBC
from odoo import http,service
from odoo import sql_db
from odoo import tools
from contextlib import closing
import logging
import lxml
import json
from psycopg2 import sql

_logger = logging.getLogger(__name__)

class DatabaseWeb(DBC):

    def _get_db_comment(self):
        db = sql_db.db_connect('postgres')
        SQL = """select db.datname,COALESCE(dsc.description,'NoComment') as comment
                from pg_catalog.pg_database db
                left join pg_catalog.pg_shdescription dsc on db.oid = dsc.objoid
                where db.datname not in ('postgres','template1','template0')"""

        with closing(db.cursor()) as cr:
            try:
                cr.execute(SQL)
                res = [[tools.ustr(x[0]),tools.ustr(x[1])] for x in cr.fetchall()]
            except Exception:
                _logger.exception('Search databases comment failed:')
                res = []
        return res

    def _update_db_comment(self, dbname, comment):
        db = sql_db.db_connect('postgres')
        with closing(db.cursor()) as cr:
            cr._cnx.autocommit = True
            try:
                cr.execute(sql.SQL("COMMENT ON DATABASE {} IS '{}'".format(dbname,comment)))
            except Exception:
                _logger.exception('Update databases comment failed:')

    def _render_template(self, **d):
        html = super(DatabaseWeb,self)._render_template(**d)
        try:
            root = lxml.etree.HTML(html)
        except ValueError:
            root = lxml.etree.HTML(html.encode('utf-8'))
        #Add button
        for item in root.xpath("//button[@data-bs-target='.o_database_backup']"):
            EleHTML="""<button type="button" data-bs-target=".o_database_comment" class="o_database_action btn btn-info" data-db="%s">
                                            <i class="fa fa-comment-o fa-fw"></i> Comment
                                        </button>
            """%(item.get('data-db'))
            item.getparent().insert(0,lxml.etree.fromstring(EleHTML))

        #Add dialog
        btnCommentDialog="""
        <div class="modal fade o_database_comment" role="dialog">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h4 class="modal-title">Comment Database</h4>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <form id="form_comment_db" role="form" action="/web/database/comment" method="post">
                        <div class="modal-body">
                            <div class="row mb-3">
                                <label for="master_pwd" class="col-md-4 col-form-label">Master Password</label>
                                <div class="col-md-8">
                                    <div class="input-group">
                                        <input name="master_pwd" id="master_pwd" required="required" autofocus="autofocus" type="password" autocomplete="current-password" class="form-control"/>
                                        <span class="fa fa-eye o_little_eye input-group-text" aria-hidden="true" style="cursor: pointer;"></span>
                                    </div>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="db_name" class="col-md-4 col-form-label">Database Name</label>
                                <div class="col-md-8">
                                    <input id="db_name" type="text" name="name" class="form-control" required="required" readonly="readonly"/>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <label for="db_comment" class="col-md-4 col-form-label">DB Comment</label>
                                <div class="col-md-8">
                                    <input id="db_comment" type="text" name="comment" class="form-control" required="required"/>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <input type="submit" value="Continue" class="btn btn-primary float-end"/>
                        </div>
                    </form>
                </div>
            </div>
        </div>"""
        root.xpath("//div[@class='container']")[0].append(lxml.etree.fromstring(btnCommentDialog))

        header_node = lxml.etree.SubElement(root.find('body'),'script')
        header_node.text = """const DBNAME = %s;
                $.each($(".list-group-item>a"),function(k,v){
                v.innerText += '-['+DBNAME[v.innerText]+']';
                });"""%json.dumps(dict(self._get_db_comment()))
        

        html = lxml.etree.tostring(root, encoding='utf-8',pretty_print =True, method="html")
    
        return html
    
    @http.route('/web/database/comment', type='http', auth="none", methods=['POST'], csrf=False)
    def dbcomment(self, master_pwd, name, comment):
        insecure = tools.config.verify_admin_password('admin')
        if insecure and master_pwd:
            http.dispatch_rpc('db', 'change_admin_password', ["admin", master_pwd])
        try:
            service.db.check_super(master_pwd)
            self._update_db_comment(name, comment)
            return http.request.redirect('/web/database/manager')
        except Exception as e:
            error = "Database comment error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)