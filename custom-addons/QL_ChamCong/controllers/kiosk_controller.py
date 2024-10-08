from odoo import http, fields
from odoo.http import request

class KioskController(http.Controller):

    @http.route('/kiosk/check_in', type='json', auth='user')
    def check_in(self, **kwargs):
        """
        API tùy chỉnh cho Kiosk Mode: Check-in thông qua mã QR
        """
        employee_id = kwargs.get('employee_id')
        if not employee_id:
            return {'error': 'Thiếu mã nhân viên'}

        # Tìm kiếm nhân viên và ghi lại thời gian check-in
        employee = request.env['ql_nhanvien.employee'].search([('id', '=', employee_id)], limit=1)
        if employee:
            check_in = request.env['ql_nhanvien.attendance'].create({
                'employee_id': employee.id,
                'check_in': fields.Datetime.now(),
                'check_in_mode': 'kiosk'
            })
            return {'success': f'{employee.name} đã check-in thành công!'}

        return {'error': 'Nhân viên không tồn tại'}
