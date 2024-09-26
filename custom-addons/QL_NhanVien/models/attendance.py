from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class EmployeeAttendance(models.Model):
    _name = 'ql_nhanvien.attendance'
    _description = 'Employee Attendance Record'

    employee_id = fields.Many2one('ql_nhanvien.employee', string='Nhân viên', required=True)
    name = fields.Many2one('ql_nhanvien.employee', string='tên ', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user.id)
    check_in = fields.Datetime(string='Giờ vào', default=lambda self: fields.Datetime.now())
    check_out = fields.Datetime(string='Giờ ra')
    check_in_time = fields.Char(string='Giờ vào (Giờ:Phút)', compute='_compute_time', store=True)
    check_out_time = fields.Char(string='Giờ ra (Giờ:Phút)', compute='_compute_time', store=True)
    fixed_time_in = fields.Char(string='Giờ vào cố định', default="08:00 AM")
    late_duration = fields.Float(string='Trễ (giờ/phút)', compute='_compute_late_duration', store=True)
    formatted_late_duration = fields.Char(string="Trễ (giờ/phút)", compute="_compute_formatted_late_duration")

    @api.depends('check_in', 'check_out')
    def _compute_time(self):
        for record in self:
            if record.check_in:
                record.check_in_time = record.check_in.strftime('%H:%M')
            if record.check_out:
                record.check_out_time = record.check_out.strftime('%H:%M')

    @api.depends('check_in')
    def _compute_late_duration(self):
        for record in self:
            if record.check_in:
                fixed_time = datetime.combine(record.check_in.date(), datetime.strptime("08:00 AM", "%I:%M %p").time())
                late_seconds = (record.check_in - fixed_time).total_seconds()
                if late_seconds > 0:
                    hours, remainder = divmod(late_seconds, 3600)
                    minutes, _ = divmod(remainder, 60)
                    record.late_duration = hours + minutes / 60.0
                else:
                    record.late_duration = 0

    @api.depends('late_duration')
    def _compute_formatted_late_duration(self):
        for record in self:
            if record.late_duration:
                hours = int(record.late_duration)
                minutes = int((record.late_duration - hours) * 60)
                record.formatted_late_duration = f"{hours} giờ {minutes} phút"
            else:
                record.formatted_late_duration = "Đúng giờ"

    @api.model
    def create(self, vals):
        if 'check_in' in vals:
            check_in_time = fields.Datetime.from_string(vals['check_in'])
        else:
            check_in_time = fields.Datetime.now()

        fixed_time = datetime.combine(check_in_time.date(), datetime.strptime("08:00 AM", "%I:%M %p").time())
        late_seconds = (check_in_time - fixed_time).total_seconds()
        if late_seconds > 0:
            hours, remainder = divmod(late_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            late_duration = hours + minutes / 60.0
        else:
            late_duration = 0

        vals['late_duration'] = late_duration

        record = super(EmployeeAttendance, self).create(vals)
        return record

    def button_check_in(self):
        self.ensure_one()
        self.create({
            'employee_id': self.employee_id.id,
            'user_id': self.env.user.id,
            'check_in': fields.Datetime.now(),
        })
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'params': {'type': 'notification', 'title': 'Check In', 'message': 'Bạn đã check in thành công!', 'sticky': False},
        }

    def button_check_out(self):
        self.ensure_one()
        self.write({'check_out': fields.Datetime.now()})
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'params': {'type': 'notification', 'title': 'Check Out', 'message': 'Bạn đã check out thành công!', 'sticky': False},
        }

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.employee_id.name} ({record.check_in.strftime('%Y-%m-%d')})"
            result.append((record.id, name))
        return result
