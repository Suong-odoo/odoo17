from odoo import models, fields, api


class Contracts(models.Model):
    _name = 'ql_nhanvien.contracts'
    _description = 'Hợp đồng nhân viên'

    # Trường cơ bản
    name = fields.Char(string='Tên hợp đồng', required=True)
    employee_id = fields.Many2one('ql_nhanvien.employee', string='Nhân viên', required=True)
    contract_type = fields.Selection([
        ('permanent', 'Hợp đồng dài hạn'),
        ('temporary', 'Hợp đồng tạm thời'),
        ('internship', 'Thực tập')
    ], string='Loại hợp đồng', required=True, default='permanent')

    start_date = fields.Date(string='Ngày bắt đầu', required=True)
    end_date = fields.Date(string='Ngày kết thúc')
    salary = fields.Float(string='Mức lương', required=True)

    state = fields.Selection([
        ('draft', 'Nháp'),
        ('active', 'Hoạt động'),
        ('terminated', 'Kết thúc')
    ], string='Trạng thái', default='draft')

    # Các trường bổ sung nếu cần
    position_name = fields.Many2one('ql_nhanvien.role', string='Vị trí công việc')
    department_id = fields.Many2one('ql_nhanvien.department', string='Phòng ban')
    notes = fields.Text(string='Ghi chú')

    # Phương thức để xác nhận hợp đồng
    def action_confirm_contract(self):
        self.state = 'active'

    # Phương thức để kết thúc hợp đồng
    def action_terminate_contract(self):
        self.state = 'terminated'

    # Kiểm tra hợp đồng đã hết hạn
    @api.depends('end_date')
    def _check_contract_expired(self):
        today = fields.Date.today()
        for contract in self:
            if contract.end_date and contract.end_date < today:
                contract.state = 'terminated'
