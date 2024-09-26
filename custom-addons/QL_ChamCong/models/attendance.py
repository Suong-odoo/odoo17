from odoo import models, fields, api
from datetime import datetime, time

class EmployeeAttendance(models.Model):
    _name = 'ql_nhanvien.attendance'
    _description = 'Employee Attendance Record'

    employee_id = fields.Many2one('ql_nhanvien.employee', string='Nhân viên', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user.id)
    check_in = fields.Datetime(string='Giờ vào', default=lambda self: fields.Datetime.now())
    check_out = fields.Datetime(string='Giờ ra')
    fixed_time_in = fields.Char(string='Giờ vào cố định', default="08:00")
    late_duration = fields.Float(string='Trễ (giờ/phút)', compute='_compute_late_duration', store=True)
    formatted_late_duration = fields.Char(string="Trễ (giờ/phút)", compute="_compute_formatted_late_duration")

    @api.depends('check_in')
    def _compute_late_duration(self):
        for record in self:
            if record.check_in:
                # Chuyển đổi giờ cố định từ chuỗi "08:00" thành đối tượng datetime
                fixed_time = datetime.combine(record.check_in.date(), time(8, 0))  # 8:00 AM
                late_seconds = (record.check_in - fixed_time).total_seconds()
                record.late_duration = late_seconds / 3600 if late_seconds > 0 else 0

    @api.depends('late_duration')
    def _compute_formatted_late_duration(self):
        for record in self:
            if record.late_duration > 0:
                hours = int(record.late_duration)
                minutes = int((record.late_duration - hours) * 60)
                record.formatted_late_duration = f"{hours} giờ {minutes} phút"
            else:
                record.formatted_late_duration = "Đúng giờ"

    @api.model
    def create(self, vals):
        """ Tính toán thời gian trễ trong quá trình tạo bản ghi """
        check_in_time = vals.get('check_in', fields.Datetime.now())
        fixed_time = datetime.combine(fields.Datetime.from_string(check_in_time).date(), datetime.strptime("08:00 AM", "%I:%M %p").time())
        late_seconds = (fields.Datetime.from_string(check_in_time) - fixed_time).total_seconds()
        vals['late_duration'] = late_seconds / 3600 if late_seconds > 0 else 0
        return super(EmployeeAttendance, self).create(vals)

    def button_check_in(self):
        """ Hành động check-in """
        self.ensure_one()
        self.create({
            'employee_id': self.employee_id.id,
            'user_id': self.env.user.id,
            'check_in': fields.Datetime.now(),
        })
        return self._send_notification('Check In', 'Bạn đã check in thành công!')

    def button_check_out(self):
        """ Hành động check-out """
        self.ensure_one()
        self.write({'check_out': fields.Datetime.now()})
        return self._send_notification('Check Out', 'Bạn đã check out thành công!')

    def _send_notification(self, title, message):
        """ Gửi thông báo sau khi check-in hoặc check-out """
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'params': {
                'type': 'notification',
                'title': title,
                'message': message,
                'sticky': False,
            },
        }

    def name_get(self):
        """ Hiển thị tên nhân viên cùng với ngày check-in """
        result = []
        for record in self:
            name = f"{record.employee_id.name} ({record.check_in.strftime('%Y-%m-%d') if record.check_in else ''})"
            result.append((record.id, name))
        return result
