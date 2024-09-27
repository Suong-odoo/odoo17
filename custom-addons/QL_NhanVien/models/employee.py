from odoo import models, fields, api
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image
from io import BytesIO
import base64
from odoo.exceptions import ValidationError


class Employee(models.Model):
    _name = 'ql_nhanvien.employee'
    _description = 'Nhân viên'
    _sql_constraints = [
        ('unique_qr_code', 'unique(qr_code)', 'Mã QR phải là duy nhất!'),
        ('unique_card_number', 'unique(card_number)', 'Mã số thẻ phải là duy nhất!'),
    ]

    # Các trường thông tin nhân viên
    name = fields.Char(string="Tên nhân viên", required=True, track_visibility='onchange')
    image = fields.Binary(string='Image', attachment=True)
    employee_id = fields.Char(string="Mã nhân viên", required=True)  # Mã nhân viên
    department_id = fields.Many2one('ql_nhanvien.department', string="Phòng ban", ondelete="cascade")
    role_ids = fields.Many2many('ql_nhanvien.role', string="Vị trí")
    work_mobile = fields.Char(string='Số điện thoại công việc')
    work_email = fields.Char(string='Email công việc', required=True)
    gender = fields.Selection([('male', 'Nam'), ('female', 'Nữ')], string='Giới tính', default='male')
    country = fields.Char(string='Quốc gia')
    domicile = fields.Char(string='Quê quán')
    day_of_birth = fields.Date(string='Ngày sinh')
    user_id = fields.Many2one('res.users', string='Người dùng', ondelete='cascade', required=True)

    # Thông tin công ty

    company_id = fields.Many2one('ql_nhanvien.company', string='Công ty', required=True)
    work_location = fields.Selection([
        ('office', 'Tại văn phòng'),
        ('home', 'Tại nhà'),
        ('other', 'Khác'),
    ], string='Địa điểm làm việc', default='office')

    work_schedule = fields.Selection([
        ('56 hours/week', '56 giờ/tuần'),
        ('48 hours/week', '48 giờ/tuần'),
        ('40 hours/week', '40 giờ/tuần'),
    ], string='Lịch làm việc')

    home_address = fields.Char(string='Địa chỉ nhà')
    personal_email = fields.Char(string='Email riêng')
    bank_account_number = fields.Char(string='Số tài khoản ngân hàng')
    education_level = fields.Selection([
        ('university', 'Đại học'),
        ('college', 'Cao đẳng'),
        ('masters', 'Thạc sĩ'),
        ('other', 'Khác')
    ], string='Cấp độ học vấn')

    degree = fields.Binary('Bằng cấp', attachment=True)
    certificate = fields.Binary('Chứng chỉ', attachment=True)
    study_field = fields.Char(string='Lĩnh vực nghiên cứu')
    school = fields.Char(string='Trường học')
    visa_number = fields.Char(string='Số Visa')
    work_permit_number = fields.Char(string='Số Giấy phép lao động')
    visa_expire_date = fields.Date(string='Ngày hết hạn Visa')
    work_permit_expire_date = fields.Date(string='Ngày hết hạn giấy phép LĐ')
    work_permit_attachment = fields.Binary(string='Giấy phép lao động')
    wage = fields.Selection([
        ('low', 'Mức thấp: 3 triệu - 5 triệu'),
        ('high', 'Mức cao: 5 triệu - 20 triệu')
    ], string='Mức lương')

    employee_type = fields.Selection([
        ('permanent', 'Nhân viên'),
        ('contract', 'Thực tập'),
        ('temporary', 'Thử việc')
    ], string='Kiểu Nhân viên')

    # Mã số thẻ và mã PIN
    card_number = fields.Char(string='Mã số Thẻ')
    ma_pin = fields.Char(string='Mã PIN')
    barcode_image = fields.Binary("Mã vạch", compute='_compute_barcode_image')

    # Tự động tạo mã PIN khi tạo mới nhân viên
    @api.model
    def create(self, vals):
        if 'ma_pin' not in vals or not vals['ma_pin']:
            vals['ma_pin'] = str(self.env['ir.sequence'].next_by_code('ql_nhanvien.employee.pin') or '').zfill(4)
        return super(Employee, self).create(vals)

    # Tạo mã vạch cho mã số thẻ
    @api.depends('card_number')
    def _compute_barcode_image(self):
        for record in self:
            if record.card_number:
                barcode_value = record.card_number
                # Tạo mã vạch
                barcode = Code128(barcode_value, writer=ImageWriter())

                # Lưu mã vạch vào buffer in-memory
                buffer = BytesIO()
                barcode.write(buffer)
                buffer.seek(0)

                # Chuyển đổi hình ảnh sang định dạng PNG
                image = Image.open(buffer)

                # Điều chỉnh kích thước nhưng giữ nguyên tỷ lệ
                aspect_ratio = image.width / image.height
                new_width = 200  # hoặc giá trị bạn mong muốn
                new_height = int(new_width / aspect_ratio)  # tính chiều cao để giữ tỷ lệ
                image = image.resize((new_width, new_height), Image.ANTIALIAS)

                # Chuyển đổi lại thành base64
                buffer_out = BytesIO()
                image.save(buffer_out, format="PNG")
                image_data = buffer_out.getvalue()
                record.barcode_image = base64.b64encode(image_data).decode('utf-8')
            else:
                record.barcode_image = False

    # Phương thức để in mã vạch hoặc thẻ nhân viên
    def action_print_employee_card(self):
        return self.env.ref('QL_NhanVien.employee_card_report').report_action(self)

    # Hàm kiểm tra số điện thoại có hợp lệ
    @api.constrains('work_mobile')
    def _check_work_mobile(self):
        for record in self:
            if record.work_mobile and (len(record.work_mobile) != 10 or not record.work_mobile.isdigit()):
                raise ValidationError("Số điện thoại phải có đúng 10 chữ số.")

    # Hàm xử lý chấm công
    attendance_ids = fields.One2many('ql_nhanvien.attendance', 'employee_id', string='Chấm công')

    def action_check_in(self):
        check_in_time = fields.Datetime.now()
        attendance = self.env['ql_nhanvien.attendance'].create({
            'employee_id': self.id,
            'check_in': check_in_time,
        })
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Bạn đã chấm công thành công.',
                'type': 'rainbow_man',
            }
        }

    def action_check_out(self):
        attendance = self.env['ql_nhanvien.attendance'].search([('employee_id', '=', self.id)], order='check_in desc', limit=1)
        if attendance and not attendance.check_out:
            check_out_time = fields.Datetime.now()
            attendance.write({'check_out': check_out_time})
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': f'Bạn đã chấm công ra lúc {check_out_time.strftime("%H:%M:%S")}',
                    'type': 'rainbow_man',
                }
            }
        else:
            return {
                'warning': {
                    'title': "Không tìm thấy bản ghi chấm công",
                    'message': "Bạn phải chấm công vào trước khi chấm công ra."
                }
            }

    # Phương thức tạo nhân viên
    def action_create_employee(self):
        for record in self:
            if not record.name:
                raise ValidationError("Tên nhân viên là bắt buộc.")
