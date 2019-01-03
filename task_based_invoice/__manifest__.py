# -*- coding: utf-8 -*-
{
    'name': "Task based Invoice",
    'summary': """
        Create invoices from task.
        """,
    'description': """
        This module creates invoices form which task are in done stage.
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Project',
    'version': '11.0.1.0.0',
    'depends': ['project', 'hr_timesheet', 'sale_management'],
    'data': [
        'views/project_task_view.xml',
        'wizard/invoice_task_rel_view.xml',
        'wizard/custom_message_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
