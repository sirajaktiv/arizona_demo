/**********************************************************************************
* 
*    Copyright (C) 2017 MuK IT GmbH
*
*    This program is free software: you can redistribute it and/or modify
*    it under the terms of the GNU Affero General Public License as
*    published by the Free Software Foundation, either version 3 of the
*    License, or (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU Affero General Public License for more details.
*
*    You should have received a copy of the GNU Affero General Public License
*    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
**********************************************************************************/

odoo.define('muk_dms_widgets.binary', function(require) {
"use strict";

var core = require('web.core');
var registry = require('web.field_registry');
var field_utils = require('web.field_utils');
var field_widgets = require('web.basic_fields');

var _t = core._t;
var QWeb = core.qweb;

var FieldDocumentBinary = field_widgets.FieldBinaryFile.extend({
	willStart: function () {
		var self = this;
		return $.when(this._super.apply(this, arguments)).then(function() {
        	return self._rpc({
                model: 'ir.attachment',
                method: 'max_upload_size',        	
                args: [],
            }).then(function(max_upload_size) {
            	var max_upload = parseInt(max_upload_size) || 25;
            	self.max_upload_size = max_upload * 1024 * 1024;
            });
        });
    },
});

registry.add('dms_binary', FieldDocumentBinary);

return FieldDocumentBinary;

});