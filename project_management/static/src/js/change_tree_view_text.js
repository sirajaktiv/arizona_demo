odoo.define('project_management.change_tree_view_text', function (require) {
"use strict";
    var core = require('web.core');
    var _t = core._t;
    var ListRenderer = require('web.ListRenderer');
    var change_text = ListRenderer.include({
        _renderRows: function () {
            var $rows = this._super();
            var base_url = this.el.baseURI
            var model = 'project.project'
            if(base_url.search(model)){
                console.log("aaaaaaaaaaaaaaaaaaaaa");
                debugger;
                .text("Add a Stage")
            }
            return $rows
        },
    });
});