import json
import logging
from odoo import http, fields, api, SUPERUSER_ID, registry
from odoo.http import request

_logger = logging.getLogger(__name__)

class EmployeeController(http.Controller):
    @http.route('/employees', auth='user', type='http', website=True)
    def list_employees(self, **kw):
        employees = request.env['ql_nhanvien.employee'].search([])
        employees_html = ''.join(
            f'<li>{emp.name} - {emp.department_id.name if emp.department_id else "N/A"} '
            f'- {emp.work_email} '
            f'- <form action="/employees/check_in" method="post"><input type="hidden" name="employee_id" value="{emp.id}"/><button type="submit">Điểm danh</button></form></li>'
            for emp in employees)
        return f'<ul>{employees_html}</ul>'

    @http.route('/employees/<string:employee_id>', auth='public', type='http', csrf=False)
    def employee_handler(self, employee_id, **kw):
        response = {"status": "error", "content": "Không tìm thấy nhân viên"}
        try:
            dbname = request.session.db
            if dbname:
                with registry(dbname).cursor() as cr:
                    env = api.Environment(cr, SUPERUSER_ID, {})
                    employee = env['ql_nhanvien.employee'].sudo().search([('employee_id', '=', employee_id)], limit=1)
                    if employee:
                        response = {
                            "status": "ok",
                            "content": {
                                "name": employee.name,
                                "department": employee.department_id.name if employee.department_id else "N/A",
                                "email": employee.work_email,
                                "mobile": employee.work_mobile,
                                "gender": dict(employee.fields_get(['gender'])['gender']['selection'])[
                                    employee.gender] if employee.gender else "N/A",
                                "country": employee.country,
                                "address": employee.home_address,
                                "birthdate": employee.day_of_birth.strftime(
                                    '%d/%m/%Y') if employee.day_of_birth else "N/A"
                            }
                        }
        except Exception as e:
            _logger.error("Lỗi khi truy cập thông tin nhân viên với ID %s: %s", employee_id, str(e))
            response = {"status": "error", "content": "Lỗi máy chủ"}

        # Chuyển đổi phản hồi thành chuỗi JSON và trả về với mã hóa UTF-8
        return http.Response(json.dumps(response, ensure_ascii=False), content_type='application/json; charset=utf-8')

    @http.route('/employees/attendance/<int:employee_id>', auth='public', type='http', csrf=False)
    def attendance_handler(self, employee_id, **kw):
        response = {"status": "error", "content": "Không tìm thấy thông tin điểm danh"}
        try:
            dbname = request.session.db
            if dbname:
                with registry(dbname).cursor() as cr:
                    env = api.Environment(cr, SUPERUSER_ID, {})
                    attendance_records = env['ql_nhanvien.attendance'].sudo().search(
                        [('employee_id', '=', employee_id)])
                    if attendance_records:
                        attendance_data = []
                        employee_name = attendance_records[0].employee_id.name if attendance_records else "N/A"
                        for record in attendance_records:
                            attendance_data.append({
                                "name": employee_name,
                                "check_in": record.check_in.strftime('%d/%m/%Y %H:%M:%S') if record.check_in else "N/A",
                                "check_out": record.check_out.strftime(
                                    '%d/%m/%Y %H:%M:%S') if record.check_out else "N/A",
                                "late_duration": record.formatted_late_duration
                            })
                        response = {
                            "status": "ok",
                            "content": attendance_data
                        }
        except Exception as e:
            _logger.error("Lỗi khi truy cập thông tin điểm danh cho nhân viên với ID %s: %s", employee_id, str(e))
            response = {"status": "error", "content": "Lỗi máy chủ"}

        # Chuyển đổi phản hồi thành chuỗi JSON và trả về với mã hóa UTF-8
        return http.Response(json.dumps(response, ensure_ascii=False), content_type='application/json; charset=utf-8')