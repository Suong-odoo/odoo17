# -*- coding: utf-8 -*-
{
    'name': "Quản lý nhân viên",
    'summary': """Mô-đun quản lý thông tin nhân viên công ty phần mềm SoftPoint""",
    'description': """
        Mô-đun quản lý thông tin nhân viên

        Mô-đun này cung cấp các tính năng để quản lý thông tin nhân viên trong công ty, bao gồm:

        - Quản lý thông tin cơ bản nhân viên như họ tên, ngày sinh, địa chỉ, số điện thoại, email, ...
        - Quản lý thông tin nghề nghiệp như vị trí công việc, phòng ban, ngày vào làm, lương, ...
        - Quản lý thông tin hợp đồng lao động, bảo hiểm, phúc lợi của nhân viên.
        - Quản lý ngày nghỉ phép, nghỉ lễ, nghỉ ốm của nhân viên.
        - Quản lý đánh giá hiệu suất làm việc và kỷ luật của nhân viên.
        - Báo cáo và thống kê về lực lượng lao động của công ty.

        Mô-đun này giúp công ty có một hệ thống quản lý nhân sự hiệu quả, đảm bảo các quy trình và chính sách liên quan đến nhân sự được tuân thủ đầy đủ.
        """,
    'author': "Group Sương and Ngân",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'base',
        'product',
        'website',

    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/employee_views.xml',
        'views/contract_view.xml',
        'report/employee_report.xml',
        'views/department_views.xml',
        'views/role_views.xml',
        'views/employee_role_views.xml',
        'views/menu_view.xml',
        'views/attendance_views.xml',
        'views/company_view.xml',
        #'data/demo_data.xml',

    ],
     'qweb': ['static/src/js/xml/qr_scanner.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
