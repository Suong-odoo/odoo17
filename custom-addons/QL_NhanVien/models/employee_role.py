import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)  # Đặt logger cho module này

class EmployeeRole(models.Model):
    _name = 'ql_nhanvien.employee_role'
    _description = 'Quan hệ vị trí nhân viên'

    name = fields.Many2one('ql_nhanvien.employee', string="Nhân viên", required=True)  # Liên kết đến bảng Employee
    employee_id = fields.Many2one('ql_nhanvien.employee', string="Mã Nhân Viên")
    role_id = fields.Many2one('ql_nhanvien.role', string="Vị trí", required=True)
    start_date = fields.Date(string="Ngày bắt đầu")
    end_date = fields.Date(string="Ngày kết thúc")

    @api.model
    def create(self, vals):
        _logger.info('Creating EmployeeRole with values: %s', vals)
        return super(EmployeeRole, self).create(vals)

    def write(self, vals):
        _logger.info('Updating EmployeeRole ID %s with values: %s', self.id, vals)
        return super(EmployeeRole, self).write(vals)
