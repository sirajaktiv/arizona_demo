# -*- coding: utf-8 -*-
{
    'name': "ITP PMS",
    'summary': """
        Manage related project's cost and progress""",
    'description': """
        Displays Project cost and progress to project manager
        and project user can views only progress of project.
    """,
    'author': "IT Principles",
    'website': "http://www.itp-ksa.com",
    'category': 'Project',
    'version': '11.0.1.0.0',
    'depends': ['sale_timesheet', 'hr_expense', 'account_invoicing',
                'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'security/project_security.xml',
        'views/project_cost_view.xml',
        'views/project_task_view.xml',
        'views/dashboard_action.xml',
        'views/project_task_type.xml',
        'views/project_view.xml',
        'views/sale_timesheet_view.xml',
        'wizard/custom_message_view.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml'
    ],
}
