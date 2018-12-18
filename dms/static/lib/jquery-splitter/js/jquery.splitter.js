///*!
// * JQuery Spliter Plugin version 0.24.0
// * Copyright (C) 2010-2016 Jakub Jankiewicz <http://jcubic.pl>
// *
// * This program is free software: you can redistribute it and/or modify
// * it under the terms of the GNU Lesser General Public License as published by
// * the Free Software Foundation, either version 3 of the License, or
// * (at your option) any later version.
// *
// * This program is distributed in the hope that it will be useful,
// * but WITHOUT ANY WARRANTY; without even the implied warranty of
// * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// * GNU Lesser General Public License for more details.
// *
// * You should have received a copy of the GNU Lesser General Public License
// * along with this program.  If not, see <http://www.gnu.org/licenses/>.
// */
//
// alert("ffffffff")
//(function($, undefined) {
//    var count = 0;
//    var splitter_id = null;
//    var splitters = [];
//    var current_splitter = null;
//    $.fn.split = function(options) {
//        var data = this.data('splitter');
//        if (data) {
//            return data;
//        }
//        var panel_1;
//        var panel_2;
//        var settings = $.extend({
//            limit: 100,
//            orientation: 'horizontal',
//            position: '50%',
//            invisible: false,
//            onDragStart: $.noop,
//            onDragEnd: $.noop,
//            onDrag: $.noop
//        }, options || {});
//        this.settings = settings;
//        var cls;
//        var children = this.children();
//        if (settings.orientation == 'vertical') {
//            panel_1 = children.first().addClass('left_panel');
//            panel_2 = panel_1.next().addClass('right_panel');
//            cls = 'vsplitter';
//        } else if (settings.orientation == 'horizontal') {
//            panel_1 = children.first().addClass('top_panel');
//            panel_2 = panel_1.next().addClass('bottom_panel');
//            cls = 'hsplitter';
//        }
//        if (settings.invisible) {
//            cls += ' splitter-invisible';
//        }
//        var width = this.width();
//        var height = this.height();
//        var id = count++;
//        this.addClass('splitter_panel');
//        var splitter = $('<div/>').addClass(cls).bind('mouseenter touchstart', function() {
//            splitter_id = id;
//        }).bind('mouseleave touchend', function() {
//            splitter_id = null;
//        }).insertAfter(panel_1);
//        var position;
//
//        function get_position(position) {
//            if (typeof position === 'number') {
//                return position;
//            } else if (typeof position === 'string') {
//                var match = position.match(/^([0-9\.]+)(px|%)$/);
//                if (match) {
//                    if (match[2] == 'px') {
//                        return +match[1];
//                    } else {
//                        if (settings.orientation == 'vertical') {
//                            return (width * +match[1]) / 100;
//                        } else if (settings.orientation == 'horizontal') {
//                            return (height * +match[1]) / 100;
//                        }
//                    }
//                } else {
//                    //throw position + ' is invalid value';
//                }
//            } else {
//                //throw 'position have invalid type';
//            }
//        }
//
//        var self = $.extend(this, {
//            refresh: function() {
//                var new_width = this.width();
//                var new_height = this.height();
//                if (width != new_width || height != new_height) {
//                    width = this.width();
//                    height = this.height();
//                    self.position(position);
//                }
//            },
//            position: (function() {
//                if (settings.orientation == 'vertical') {
//                    return function(n, silent) {
//                        if (n === undefined) {
//                            return position;
//                        } else {
//                            position = get_position(n);
//                            var sw = splitter.width();
//                            var sw2 = sw/2, pw;
//                            if (settings.invisible) {
//                                pw = panel_1.width(position).outerWidth();
//                                panel_2.width(self.width()-pw);
//                                splitter.css('left', pw-sw2);
//                            } else {
//                                pw = panel_1.width(position-sw2).outerWidth();
//                                panel_2.width(self.width()-pw-sw);
//                                splitter.css('left', pw);
//                            }
//                            panel_1.find('.splitter_panel').eq(0).height(self.height());
//                            panel_2.find('.splitter_panel').eq(0).height(self.height());
//                        }
//                        if (!silent) {
//                            self.trigger('splitter.resize');
//                            self.find('.splitter_panel').trigger('splitter.resize');
//                        }
//                        return self;
//                    };
//                } else if (settings.orientation == 'horizontal') {
//                    return function(n, silent) {
//                        if (n === undefined) {
//                            return position;
//                        } else {
//                            position = get_position(n);
//                            var sw = splitter.height();
//                            var sw2 = sw/2, pw;
//                            if (settings.invisible) {
//                                pw = panel_1.height(position).outerHeight();
//                                panel_2.height(self.height()-pw);
//                                splitter.css('top', pw-sw2);
//                            } else {
//                                pw = panel_1.height(position-sw2).outerHeight();
//                                panel_2.height(self.height()-pw-sw);
//                                splitter.css('top', pw);
//                            }
//                        }
//                        if (!silent) {
//                            self.trigger('splitter.resize');
//                            self.find('.splitter_panel').trigger('splitter.resize');
//                        }
//                        return self;
//                    };
//                } else {
//                    return $.noop;
//                }
//            })(),
//            orientation: settings.orientation,
//            limit: settings.limit,
//            isActive: function() {
//                return splitter_id === id;
//            },
//            destroy: function() {
//                self.removeClass('splitter_panel');
//                splitter.unbind('mouseenter');
//                splitter.unbind('mouseleave');
//                splitter.unbind('touchstart');
//                splitter.unbind('touchmove');
//                splitter.unbind('touchend');
//                splitter.unbind('touchleave');
//                splitter.unbind('touchcancel');
//                if (settings.orientation == 'vertical') {
//                    panel_1.removeClass('left_panel');
//                    panel_2.removeClass('right_panel');
//                } else if (settings.orientation == 'horizontal') {
//                    panel_1.removeClass('top_panel');
//                    panel_2.removeClass('bottom_panel');
//                }
//                self.unbind('splitter.resize');
//                self.trigger('splitter.resize');
//                self.find('.splitter_panel').trigger('splitter.resize');
//                splitters[id] = null;
//                count--;
//                splitter.remove();
//                self.removeData('splitter');
//                var not_null = false;
//                for (var i=splitters.length; i--;) {
//                    if (splitters[i] !== null) {
//                        not_null = true;
//                        break;
//                    }
//                }
//                //remove document events when no splitters
//                if (!not_null) {
//                    $(document.documentElement).unbind('.splitter');
//                    $(window).unbind('resize.splitter');
//                    splitters = [];
//                    count = 0;
//                }
//            }
//        });
//        self.bind('splitter.resize', function(e) {
//            var pos = self.position();
//            if (self.orientation == 'vertical' &&
//                pos > self.width()) {
//                pos = self.width() - self.limit-1;
//            } else if (self.orientation == 'horizontal' &&
//                       pos > self.height()) {
//                pos = self.height() - self.limit-1;
//            }
//            if (pos < self.limit) {
//                pos = self.limit + 1;
//            }
//            e.stopPropagation();
//            self.position(pos, true);
//        });
//        //inital position of splitter
//        var pos;
//        if (settings.orientation == 'vertical') {
//            if (pos > width-settings.limit) {
//                pos = width-settings.limit;
//            } else {
//                pos = get_position(settings.position);
//            }
//        } else if (settings.orientation == 'horizontal') {
//            //position = height/2;
//            if (pos > height-settings.limit) {
//                pos = height-settings.limit;
//            } else {
//                pos = get_position(settings.position);
//            }
//        }
//        if (pos < settings.limit) {
//            pos = settings.limit;
//        }
//        self.position(pos, true);
//		var parent = this.closest('.splitter_panel');
//        if (parent.length) {
//            this.height(parent.height());
//        }
//        // bind events to document if no splitters
//        if (splitters.filter(Boolean).length === 0) {
//            $(window).bind('resize.splitter', function() {
//                $.each(splitters, function(i, splitter) {
//                    if (splitter) {
//                        splitter.refresh();
//                    }
//                });
//            });
//            $(document.documentElement).on('mousedown.splitter touchstart.splitter', function(e) {
//                if (splitter_id !== null) {
//                    e.preventDefault();
//                    current_splitter = splitters[splitter_id];
//                    setTimeout(function() {
//                        $('<div class="splitterMask"></div>').
//                            css('cursor', current_splitter.children().eq(1).css('cursor')).
//                            insertAfter(current_splitter);
//                    });
//                    current_splitter.settings.onDragStart(e);
//                }
//            }).bind('mouseup.splitter touchend.splitter touchleave.splitter touchcancel.splitter', function(e) {
//                if (current_splitter) {
//                    setTimeout(function() {
//                        $('.splitterMask').remove();
//                    });
//                    current_splitter.settings.onDragEnd(e);
//                    current_splitter = null;
//                }
//            }).bind('mousemove.splitter touchmove.splitter', function(e) {
//                if (current_splitter !== null) {
//                    var limit = current_splitter.limit;
//                    var offset = current_splitter.offset();
//                    if (current_splitter.orientation == 'vertical') {
//                        var pageX = e.pageX;
//                        if(e.originalEvent && e.originalEvent.changedTouches){
//                          pageX = e.originalEvent.changedTouches[0].pageX;
//                        }
//                        var x = pageX - offset.left;
//                        if (x <= current_splitter.limit) {
//                            x = current_splitter.limit + 1;
//                        } else if (x >= current_splitter.width() - limit) {
//                            x = current_splitter.width() - limit - 1;
//                        }
//                        if (x > current_splitter.limit &&
//                            x < current_splitter.width()-limit) {
//                            current_splitter.position(x, true);
//                            current_splitter.trigger('splitter.resize');
//                            current_splitter.find('.splitter_panel').
//                                trigger('splitter.resize');
//                            //e.preventDefault();
//                        }
//                    } else if (current_splitter.orientation == 'horizontal') {
//                        var pageY = e.pageY;
//                        if(e.originalEvent && e.originalEvent.changedTouches){
//                          pageY = e.originalEvent.changedTouches[0].pageY;
//                        }
//                        var y = pageY-offset.top;
//                        if (y <= current_splitter.limit) {
//                            y = current_splitter.limit + 1;
//                        } else if (y >= current_splitter.height() - limit) {
//                            y = current_splitter.height() - limit - 1;
//                        }
//                        if (y > current_splitter.limit &&
//                            y < current_splitter.height()-limit) {
//                            current_splitter.position(y, true);
//                            current_splitter.trigger('splitter.resize');
//                            current_splitter.find('.splitter_panel').
//                                trigger('splitter.resize');
//                            //e.preventDefault();
//                        }
//                    }
//                    current_splitter.settings.onDrag(e);
//                }
//            });//*/
//        }
//        splitters[id] = self;
//        self.data('splitter', self);
//        return self;
//    };
//})(jQuery);


/*
 * jQuery.splitter.js - two-pane splitter window plugin
 *
 * version 1.51 (2009/01/09)
 *
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 */

/**
 * The splitter() plugin implements a two-pane resizable splitter window.
 * The selected elements in the jQuery object are converted to a splitter;
 * each selected element should have two child elements, used for the panes
 * of the splitter. The plugin adds a third child element for the splitbar.
 *
 * For more details see: http://methvin.com/splitter/
 *
 *
 * @example $('#MySplitter').splitter();
 * @desc Create a vertical splitter with default settings
 *
 * @example $('#MySplitter').splitter({type: 'h', accessKey: 'M'});
 * @desc Create a horizontal splitter resizable via Alt+Shift+M
 *
 * @name splitter
 * @type jQuery
 * @param Object options Options for the splitter (not required)
 * @cat Plugins/Splitter
 * @return jQuery
 * @author Dave Methvin (dave.methvin@gmail.com)
 */
 ;(function($){

 $.fn.splitter = function(args){
        args = args || {};
        return this.each(function() {
                var zombie;             // left-behind splitbar for outline resizes
                function startSplitMouse(evt) {
                        if ( opts.outline )
                                zombie = zombie || bar.clone(false).insertAfter(A);
                        panes.css("-webkit-user-select", "none");       // Safari selects A/B text on a move
                        bar.addClass(opts.activeClass);
                        A._posSplit = A[0][opts.pxSplit] - evt[opts.eventPos];
                        $(document)
                                .bind("mousemove", doSplitMouse)
                                .bind("mouseup", endSplitMouse);
                }
                function doSplitMouse(evt) {
                        var newPos = A._posSplit+evt[opts.eventPos];
                        if ( opts.outline ) {
                                newPos = Math.max(0, Math.min(newPos, splitter._DA - bar._DA));
                                bar.css(opts.origin, newPos);
                        } else
                                resplit(newPos);
                }
                function endSplitMouse(evt) {
                        bar.removeClass(opts.activeClass);
                        var newPos = A._posSplit+evt[opts.eventPos];
                        if ( opts.outline ) {
                                zombie.remove(); zombie = null;
                                resplit(newPos);
                        }
                        panes.css("-webkit-user-select", "text");       // let Safari select text again
                        $(document)
                                .unbind("mousemove", doSplitMouse)
                                .unbind("mouseup", endSplitMouse);
                }
                function resplit(newPos) {
                        // Constrain new splitbar position to fit pane size limits
                        newPos = Math.max(A._min, splitter._DA - B._max,
                                        Math.min(newPos, A._max, splitter._DA - bar._DA - B._min));
                        // Resize/position the two panes
                        bar._DA = bar[0][opts.pxSplit];         // bar size may change during dock
                        bar.css(opts.origin, newPos).css(opts.fixed, splitter._DF);
                        A.css(opts.origin, 0).css(opts.split, newPos).css(opts.fixed,  splitter._DF);
                        B.css(opts.origin, newPos+bar._DA)
                                .css(opts.split, splitter._DA-bar._DA-newPos).css(opts.fixed,  splitter._DF);
                        // IE fires resize for us; all others pay cash
                        if ( !$.browser.msie )
                                panes.trigger("resize");
                }
                function dimSum(jq, dims) {
                        // Opera returns -1 for missing min/max width, turn into 0
                        var sum = 0;
                        for ( var i=1; i < arguments.length; i++ )
                                sum += Math.max(parseInt(jq.css(arguments[i])) || 0, 0);
                        return sum;
                }

                // Determine settings based on incoming opts, element classes, and defaults
                var vh = (args.splitHorizontal? 'h' : args.splitVertical? 'v' : args.type) || 'v';
                var opts = $.extend({
                        activeClass: 'active',  // class name for active splitter
                        pxPerKey: 8,                    // splitter px moved per keypress
                        tabIndex: 0,                    // tab order indicator
                        accessKey: ''                   // accessKey for splitbar
                },{
                        v: {                                    // Vertical splitters:
                                keyLeft: 39, keyRight: 37, cursor: "e-resize",
                                splitbarClass: "vsplitbar", outlineClass: "voutline",
                                type: 'v', eventPos: "pageX", origin: "left",
                                split: "width",  pxSplit: "offsetWidth",  side1: "Left", side2: "Right",
                                fixed: "height", pxFixed: "offsetHeight", side3: "Top",  side4: "Bottom"
                        },
                        h: {                                    // Horizontal splitters:
                                keyTop: 40, keyBottom: 38,  cursor: "n-resize",
                                splitbarClass: "hsplitbar", outlineClass: "houtline",
                                type: 'h', eventPos: "pageY", origin: "top",
                                split: "height", pxSplit: "offsetHeight", side1: "Top",  side2: "Bottom",
                                fixed: "width",  pxFixed: "offsetWidth",  side3: "Left", side4: "Right"
                        }
                }[vh], args);

                // Create jQuery object closures for splitter and both panes
                var splitter = $(this).css({position: "relative"});
                var panes = $(">*", splitter[0]).css({
                        position: "absolute",                   // positioned inside splitter container
                        "z-index": "1",                                 // splitbar is positioned above
                        "-moz-outline-style": "none"    // don't show dotted outline
                });
                var A = $(panes[0]);            // left  or top
                var B = $(panes[1]);            // right or bottom

                // Focuser element, provides keyboard support; title is shown by Opera accessKeys
                var focuser = $('<a href="javascript:void(0)"></a>')
                        .attr({accessKey: opts.accessKey, tabIndex: opts.tabIndex, title: opts.splitbarClass})
                        .bind($.browser.opera?"click":"focus", function(){ this.focus(); bar.addClass(opts.activeClass) })
                        .bind("keydown", function(e){
                                var key = e.which || e.keyCode;
                                var dir = key==opts["key"+opts.side1]? 1 : key==opts["key"+opts.side2]? -1 : 0;
                                if ( dir )
                                        resplit(A[0][opts.pxSplit]+dir*opts.pxPerKey, false);
                        })
                        .bind("blur", function(){ bar.removeClass(opts.activeClass) });

                // Splitbar element, can be already in the doc or we create one
                var bar = $(panes[2] || '<div></div>')
                        .insertAfter(A).css("z-index", "100").append(focuser)
                        .attr({"class": opts.splitbarClass, unselectable: "on"})
                        .css({position: "absolute",     "user-select": "none", "-webkit-user-select": "none",
                                "-khtml-user-select": "none", "-moz-user-select": "none"})
                        .bind("mousedown", startSplitMouse);
                // Use our cursor unless the style specifies a non-default cursor
                if ( /^(auto|default|)$/.test(bar.css("cursor")) )
                        bar.css("cursor", opts.cursor);

                // Cache several dimensions for speed, rather than re-querying constantly
                bar._DA = bar[0][opts.pxSplit];
                splitter._PBF = $.boxModel? dimSum(splitter, "border"+opts.side3+"Width", "border"+opts.side4+"Width") : 0;
                splitter._PBA = $.boxModel? dimSum(splitter, "border"+opts.side1+"Width", "border"+opts.side2+"Width") : 0;
                A._pane = opts.side1;
                B._pane = opts.side2;
                $.each([A,B], function(){
                        this._min = opts["min"+this._pane] || dimSum(this, "min-"+opts.split);
                        this._max = opts["max"+this._pane] || dimSum(this, "max-"+opts.split) || 9999;
                        this._init = opts["size"+this._pane]===true ?
                                parseInt($.curCSS(this[0],opts.split)) : opts["size"+this._pane];
                });

                // Determine initial position, get from cookie if specified
                var initPos = A._init;
                if ( !isNaN(B._init) )  // recalc initial B size as an offset from the top or left side
                        initPos = splitter[0][opts.pxSplit] - splitter._PBA - B._init - bar._DA;
                if ( opts.cookie ) {
                        if ( !$.cookie )
                                alert('jQuery.splitter(): jQuery cookie plugin required');
                        var ckpos = parseInt($.cookie(opts.cookie));
                        if ( !isNaN(ckpos) )
                                initPos = ckpos;
                        $(window).bind("unload", function(){
                                var state = String(bar.css(opts.origin));       // current location of splitbar
                                $.cookie(opts.cookie, state, {expires: opts.cookieExpires || 365,
                                        path: opts.cookiePath || document.location.pathname});
                        });
                }
                if ( isNaN(initPos) )   // King Solomon's algorithm
                        initPos = Math.round((splitter[0][opts.pxSplit] - splitter._PBA - bar._DA)/2);

                // Resize event propagation and splitter sizing
                if ( opts.anchorToWindow ) {
                        // Account for margin or border on the splitter container and enforce min height
                        splitter._hadjust = dimSum(splitter, "borderTopWidth", "borderBottomWidth", "marginBottom");
                        splitter._hmin = Math.max(dimSum(splitter, "minHeight"), 20);
                        $(window).bind("resize", function(){
                                var top = splitter.offset().top;
                                var wh = $(window).height();
                                splitter.css("height", Math.max(wh-top-splitter._hadjust, splitter._hmin)+"px");
                                if ( !$.browser.msie ) splitter.trigger("resize");
                        }).trigger("resize");
                }
                else if ( opts.resizeToWidth && !$.browser.msie )
                        $(window).bind("resize", function(){
                                splitter.trigger("resize");
                        });

                // Resize event handler; triggered immediately to set initial position
                splitter.bind("resize", function(e, size){
                        // Custom events bubble in jQuery 1.3; don't Yo Dawg
                        if ( e.target != this ) return;
                        // Determine new width/height of splitter container
                        splitter._DF = splitter[0][opts.pxFixed] - splitter._PBF;
                        splitter._DA = splitter[0][opts.pxSplit] - splitter._PBA;
                        // Bail if splitter isn't visible or content isn't there yet
                        if ( splitter._DF <= 0 || splitter._DA <= 0 ) return;
                        // Re-divvy the adjustable dimension; maintain size of the preferred pane
                        resplit(!isNaN(size)? size : (!(opts.sizeRight||opts.sizeBottom)? A[0][opts.pxSplit] :
                                splitter._DA-B[0][opts.pxSplit]-bar._DA));
                }).trigger("resize" , [initPos]);
        });
};

 })(jQuery);

