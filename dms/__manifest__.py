# -*- coding: utf-8 -*-
{
    'name': "Document Management System",
    'summary': """
        This module diplay graphical structure of projects
        and it's attachments.""",
    'description': """
        No need to download attched pdf documents of project and task.
        User can easily view in documents menu.
    """,
    'author': "IT Principles",
    'website': "http://www.itp-ksa.com",
    'category': 'Document',
    'version': '11.0.1.0.0',
    'depends': ['project_management', 'muk_web_preview',
                'document', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'security/directory_security.xml',
        'views/add_js.xml',
        'data/data.xml',
        'views/dms_directory_views.xml',
        'views/tree_view_action_views.xml',
        'views/project_task_view.xml',
    ],
    'qweb': [
        "static/src/xml/tree_view.xml",
        "static/src/xml/dms_widgets.xml",
    ],
}
