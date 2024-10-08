# -*- coding: utf-8 -*-
{
    'name': "Quản lý Chấm Công",
    'summary': """Mô-đun quản lý chấm công cho nhân viên công ty phần mềm SoftPoint""",
    'description': """
        Mô-đun Quản lý Chấm Công

        Mô-đun này cung cấp các tính năng để quản lý chấm công của nhân viên trong công ty, bao gồm:

        - Ghi nhận thời gian check-in và check-out của nhân viên
        - Tính toán tự động số giờ làm việc dựa trên thời gian check-in và check-out
        - Theo dõi đi muộn, về sớm và làm thêm giờ
        - Tích hợp với module Quản lý Nhân viên để liên kết thông tin chấm công với hồ sơ nhân viên
        - Tạo báo cáo chấm công theo ngày, tuần, tháng
        - Hỗ trợ xuất dữ liệu chấm công để tính lương
        - Giao diện thân thiện cho nhân viên tự chấm công
        - Tích hợp với các thiết bị chấm công (tùy chọn)

        Mô-đun này giúp công ty quản lý thời gian làm việc của nhân viên một cách hiệu quả, 
        đảm bảo tính chính xác trong việc tính toán giờ làm và hỗ trợ cho quá trình tính lương.
        """,
    'author': "Group Sương and Ngân",
    'category': 'Human Resources',
    'version': '0.1',
    'depends': [
        'QL_NhanVien',
        'base',
        'web',

    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/attendance_view.xml',
        'views/attendance_kiosk_view.xml',
    ],
     'assets': {

    },
    'installable': True,
    'application': True,
    'auto_install': False,
}