from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class Contract(models.Model):
    _name = 'ql_nhanvien.contract'
    _description = 'Hợp đồng lao động'

    contract_name = fields.Char(string="Tên hợp đồng", required=True)
    employee_id = fields.Many2one('ql_nhanvien.employee', string="Nhân viên", required=True)
    start_date = fields.Date(string="Ngày bắt đầu", required=True)
    end_date = fields.Date(string="Ngày kết thúc")
    wage = fields.Float(string="Lương tổng", required=True)
    status = fields.Selection([
        ('draft', 'Nháp'),
        ('active', 'Hoạt động'),
        ('terminated', 'Đã chấm dứt'),
    ], string="Trạng thái", default='draft')

    contract_type = fields.Selection([
        ('permanent', 'Hợp đồng chính thức'),
        ('temporary', 'Hợp đồng tạm thời'),
        ('intern', 'Hợp đồng thực tập'),
    ], string="Loại hợp đồng", required=True, default='permanent')

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.end_date and record.start_date > record.end_date:
                raise ValidationError("Ngày kết thúc không thể trước ngày bắt đầu.")

    @api.model
    def create(self, vals):
        if vals.get('employee_id'):
            employee = self.env['ql_nhanvien.employee'].browse(vals['employee_id'])
            vals['contract_name'] = f"Hợp đồng của {employee.name}"
        return super(Contract, self).create(vals)

    def action_confirm_contract(self):
        self.status = 'active'

    def action_terminate_contract(self):
        self.status = 'terminated'
