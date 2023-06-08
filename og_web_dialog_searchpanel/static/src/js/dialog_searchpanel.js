/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {SelectCreateDialog} from "@web/views/view_dialogs/select_create_dialog";

patch(SelectCreateDialog.prototype, "og_web_dialog_searchpanel.SelectCreateDialog", {
    setup() {
        this._super(...arguments);
        this.baseViewProps = Object.assign(this.baseViewProps, {display: { searchPanel: true }});
    }
});