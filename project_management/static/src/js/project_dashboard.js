odoo.define('itp_project_dashboard', function(require) {
"use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;

    var project_dashboard = Widget.extend({
        template: 'project_details_dashboard',
        init: function(parent, context) {
            var self = this;
            this._super(parent, context);
            this.active_id = context.context.active_id;
        },
        start: function() {
            var self = this;
            self.get_project_details();
            self.get_project_task_pie_chart();
            self.get_project_task_bar_chart();
            self.get_project_progress_details();
            self.get_project_timesheet_details();
            return this._super();
        },
        get_project_task_pie_chart: function(){
            var self = this;
            self._rpc({
                model: "project.task",
                method: "get_progress_task",
                args: [[self.active_id]],
            })
            .then(function (res) {
                self.task_recs = res;
                self.graph()
            });
        },
        get_project_task_bar_chart: function(){
            var self = this;
            self._rpc({
                model: "project.task",
                method: "get_task_not_completed",
                args: [[self.active_id]],
            })
            .then(function (timesheet) {
                self.task_chart = timesheet;
                self.bar_chart()
            });
        },
        bar_chart: function(){
            var self = this;
            var progress_bar = this.$el.find("#myBar");
            var progress_bar2 = this.$el.find("#myBar2");
            if(self.task_chart != 'undefined'){
                progress_bar.css({'width':self.task_chart['lately_completed']+"%"});
                progress_bar2.css({'width':self.task_chart['not_started']+"%"});
            }
        },
        get_project_progress_details: function(){
            var self = this;
            self._rpc({
                model: "project.project",
                method: "get_stage_progress",
                args: [[self.active_id]],
            })
            .then(function (res) {
                self.project_stage_progress = res;
                var stage_progress = $(QWeb.render('project_stage_progress',{
                    stage_data: self.project_stage_progress
                }));
                self.$('.stage_progress').append(stage_progress);
            });
        },
        get_project_details: function(){
            var self = this;
            self._rpc({
                model: 'project.project',
                method: 'get_current_project_details',
                args: [[self.active_id]]
            }).then(function(result){
                self.project_details = result[0]
                self.href = window.location.href;
                var linewidget = $(QWeb.render('project_form_details',{
                    widget:self.project_details,
                }));
                var pro_issue = $(QWeb.render('issues_and_risk',{
                    widget:self.project_details,
                }));
                var cost_data = $(QWeb.render('cost_chart',{
                    cost_recs :self.project_details,
                }));
                self.$('.chart-note-wrap').append(cost_data);
                self.$('.project_form_view').append(linewidget);
                self.$('.issues-and-risk').append(pro_issue);
                self.get_cost_details();
            });
        },
        get_project_timesheet_details: function(){
            var self = this;
            self._rpc({
                model: "account.analytic.line",
                method: "get_timesheet_entries",
                args: [[self.active_id]],
            })
            .then(function (timesheet) {
                self.timesheet_recs = timesheet;
                var timesheet = $(QWeb.render('timesheet_records',{
                    ts_recs:self.timesheet_recs,
                }));
                self.$('.timesheet_recs').append(timesheet);
            });
        },
        graph: function() {
            var self = this;
            var piectx = this.$el.find('#progress_pie_chart');
            var bg_color_list = ['#CE5353','#E4E4E4','#7ABD6B','#e5df39']
            if(self.task_recs != 'undefined'){
                var pieChart = new Chart(piectx, {
                    type: 'pie',
                    data: {
                        datasets: [{
                            data: self.task_recs.task_progress,
                            backgroundColor: bg_color_list,
                            label: 'Progress Pie'
                        }],
                        labels: self.task_recs.task_status,
                    },
                    options: {
                        responsive: true
                    }
                });
            }
        },
        get_cost_details: function(){
            var self = this;
            var ctx = this.$el.find("#percent-chart");
            var not_used = self.project_details.overall_project_cost - (self.project_details.overall_project_cost * self.project_details.total_cost) / 100;
            if(not_used < 0){
                not_used = 0;
            }
            ctx.height = 280;
            var myChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    datasets: [{
                        label: "My First dataset",
                        data: [(self.project_details.overall_project_cost * self.project_details.total_cost) / 100, not_used],
                        backgroundColor: [
                            '#ba1a24',
                            '#1c9607'
                        ],
                        hoverBackgroundColor: [
                            '#ba1a24',
                            '#1c9607'
                        ],
                        borderWidth: [
                            0, 0
                        ],
                        hoverBorderColor: [
                            'transparent',
                            'transparent'
                        ]
                    }],
                    labels: [
                        'Used Cost',
                        'Not Used Cost'
                    ]
                },
                options: {
                    maintainAspectRatio: false,
                    responsive: true,
                    cutoutPercentage: 55,
                    animation: {
                        animateScale: true,
                        animateRotate: true
                    },
                    legend: {
                        display: false
                    },
                    tooltips: {
                        titleFontFamily: "Poppins",
                        xPadding: 15,
                        yPadding: 10,
                        caretPadding: 0,
                        bodyFontSize: 16
                    }
                }
            });
        },
    });

    core.action_registry.add('itp_project_dashboard', project_dashboard);

    return project_dashboard
});