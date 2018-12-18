odoo.define('dms.tree_view_directory', function(require) {
"use strict";

    var core = require('web.core');
    var session = require('web.session');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');
    var session = require('web.session');
    var PreviewHelper = require('muk_dms_preview_file.PreviewHelper');
    var QWeb = core.qweb;

    var open = function(self, model, id) {
        self.do_action({
            type: 'ir.actions.act_window',
            res_model: model,
            res_id: id,
            views: [[false, 'form']],
            target: 'current',
            context: session.user_context,
            flags: {'form': {'action_buttons': 'True', 'options': {'clear_breadcrumbs':'True' } } }
        });
        
    }

    var create = function(self, model, parent) {
        var context = {};
        if(model == "ir.attachment") {
            context = $.extend(session.user_context, {
                default_dms_directory_id: parent
            });
        } else if(model == "dms.directory") {
            context = $.extend(session.user_context, {
                default_parent_directory_id: parent
            });
        }
        self.do_action({
            type: 'ir.actions.act_window',
            res_model: "dms.directory",
            views: [[false, 'form']],
            target: 'current',
            context: context,
            flags: {'form': {'action_buttons': 'True', 'options': {'clear_breadcrumbs':'True' } } }
        });
    }

    var context_menu_items = function(node, cp) {}

    var DMS_TREE_VIEW = Widget.extend({
        template: 'DocumentTreeView',
        events: {
            "click button.open": "open",
            "click button.create_directory": "create_directory",
        },

        init: function(parent, action) {
            this._super(parent, action);
            this.session = session;
            this.uid = session.uid
            this.splitter = false;
            this.auto_refresh = true;
            this.action_open_dialog = false;
            this.name = 'Document Tree';
        },
        start: function () {
            var self = this;
            self.session = session;
            self.show_directory_view();
            self.update_cp();
            $( ".o_control_panel" ).addClass( "o_hidden" );
        },

        update_cp: function() {
            if (!this.$switch_buttons) {
                this.$switch_buttons = $(QWeb.render('dms.DocumentTreeViewOptions', {
                    widget: this,
                }));
            }
        },

        add_all_directories: function(self) {
            self.user_id = self.session.uid;
            var directories_query = $.Deferred();
            rpc.query({
                model: 'dms.directory',
                method: 'search_read',
            }).then(function (directories) {
                var data = [];
                var directory_ids = _.map(directories, function(directory, index) {
                    return directory.id;
                });
                _.each(directories, function(value, key, list) {
                    data.push({
                        id: "directory_" + value.id,
                        parent: (value.parent_directory_id && $.inArray(value.parent_directory_id[0], directory_ids) !== -1 ? "directory_" + value.parent_directory_id[0] : "#"),
                        text: value.name,
                        icon: "fa fa-folder-o",
                        type: "directory",
                        data: {
                            container: false,
                            odoo_id: value.id,
                            odoo_parent_id: value.parent_directory_id[0],
                            odoo_model: "dms.directory",
                            name: value.name,
                            directories: value.total_child_directories,
                        }
                    });
                });
                directories_query.resolve(data, directory_ids);
            });
            return directories_query;
        },
        add_all_files: function(self, directory_ids) {
            var files_query = $.Deferred();
            rpc.query({
                model: 'ir.attachment',
                method: 'get_documents'
            }).then(function (files) {
                var data = [];
                _.each(files, function(value, key, list) {
                    if(!($.inArray(value.dms_directory_id, directory_ids) !== -1)) {
                        directory_ids.push(value.dms_directory_id);
                    }
                    data.push({
                        id: "file," + value.id,
                        parent: "directory_" + value.dms_directory_id,
                        text: value.name,
                        icon: font_awesome_file_icon(value.mimetype),
                        type: "file",
                        data: {
                            odoo_id: value.id,
                            odoo_parent_id: value.dms_directory_id,
                            odoo_model: "ir.attachment",
                            filename: value.name,
                        }
                    });
                });
                files_query.resolve(data);
            });
            return files_query;
        },
        show_directory_view: function() {
            var self = this;
            $.when(self.add_all_directories(self)).done(function (directories, directory_ids) {
                $.when(self.add_all_files(self, directory_ids)).done(function (files) {
                    var data = directories.concat(files);
                    self.$el.find('.oe_document_tree').jstree({
                        'widget': self,
                        'core': {
                            'animation': 0,
                            'multiple': false,
                            'check_callback': true,
                            'themes': { "icons": true },
                            'data': data
                        },
                        'plugins': [
                            "contextmenu", "search", "sort", "state", "wholerow", "types"
                        ],
                        'contextmenu': {
                            items: context_menu_items
                        },
                    }).on('open_node.jstree', function (e, data) {
                        data.instance.set_icon(data.node, "fa fa-folder-open-o");
                    }).on('close_node.jstree', function (e, data) {
                        data.instance.set_icon(data.node, "fa fa-folder-o");
                    }).bind('loaded.jstree', function(e, data) {
                        self.show_preview();
                    }).on('changed.jstree', function (e, data) {
                        self.selected_node = data.node;
                        self._update_jstree(data);
                    });
                    var timeout = false;
                });
            });
        },
        _preview_node: function(node) {
            var self = this;

            if(node.data && node.data.odoo_model === "ir.attachment") {
                PreviewHelper.createFilePreviewContent(node.data.odoo_id, self).then(function($content) {
                    self.$el.find('.open').addClass( "o_hidden" );
                    self.$el.find('.oe_document_preview').html($content);
                });
            } else if(node.data && node.data.odoo_model === "dms.directory") {
                self.$el.find('.open').removeClass( "o_hidden" );
                self.$el.find('.oe_document_preview').html(
                        $(QWeb.render('dms.DocumentTreeViewDirectoryPreview', {
                            widget: this,
                            directory: node.data,
                        })));
            }
        },

        _update_jstree: function(data) {
            if(data.action === "select_node" && data.node) {
                if(data.selected.length === 1) {
                    if(this.show_preview_active) {
                        this._preview_node(data.node);
                    }
                }
            }
            $("#menuContinenti").prop('disabled', function (_, val) { return ! val; });
        },

        show_preview: function() {
            this.show_preview_active = true;
             if(!this.$switch_buttons.parent().find('.show_preview').hasClass("active")) {
                 this.$switch_buttons.parent().find('.show_preview').addClass("active");
                 this.$switch_buttons.parent().find('.hide_preview').removeClass("active");
                 this.$el.find('.oe_document_col_preview').show();
                 $(".oe_document_row").splitter();
             }
        },
        open: function() {
            if(this.selected_node) {
                if(this.selected_node.data.odoo_model == "dms.directory"){
                    open(this, this.selected_node.data.odoo_model, this.selected_node.data.odoo_id);
                }
            }
        },
        create_directory: function() {
            if(this.selected_node) {
                if(this.selected_node.data.odoo_model == "dms.directory") {
                    create(this, "dms.directory", this.selected_node.data.odoo_id);
                } else {
                    create(this, "ir.attachment", this.selected_node.data.odoo_id);
                }
            }
            else{
                create(this, "dms.directory",0);
            }
        },
    });

    core.action_registry.add('dms.tree_view_directory', DMS_TREE_VIEW);

    return DMS_TREE_VIEW
});