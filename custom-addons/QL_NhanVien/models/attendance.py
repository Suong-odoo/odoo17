from odoo import api, fields, models

class Attendance(models.Model):
    _name = 'ql_nhanvien.attendance'
    _description = 'Chấm công'

    check_in = fields.Datetime(string="Giờ vào")
    check_out = fields.Datetime(string="Giờ ra")
    employee_id = fields.Many2one('ql_nhanvien.employee', string='Nhân viên', required=True)
    hours_worked = fields.Float(string='Số giờ làm việc', compute='_compute_hours_worked', store=True)
    extra_hours = fields.Float(string='Giờ làm thêm', compute='_compute_extra_hours', store=True)
    image = fields.Binary(related='employee_id.image', string="Hình ảnh nhân viên", store=True)

    # Thêm chế độ chấm công với nhãn tiếng Việt
    check_in_mode = fields.Selection([
        ('manual', 'Thủ công'),
        ('automatic', 'Kiosk Mode')
    ], string='Chế độ chấm công', default='manual', required=True, help='Chọn chế độ chấm công: thủ công hoặc tự động.')

    @api.depends('check_in', 'check_out')
    def _compute_hours_worked(self):
        for record in self:
            if record.check_in and record.check_out:
                delta = record.check_out - record.check_in
                record.hours_worked = delta.total_seconds() / 3600
            else:
                record.hours_worked = 0.0

    @api.depends('hours_worked', 'employee_id.standard_hours')
    def _compute_extra_hours(self):
        for record in self:
            standard_hours = record.employee_id.standard_hours
            if record.hours_worked > standard_hours:
                record.extra_hours = record.hours_worked - standard_hours
            else:
                record.extra_hours = 0.0
