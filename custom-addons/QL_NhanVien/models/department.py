from odoo import models, fields

class Department(models.Model):
    _name = 'ql_nhanvien.department'
    _description = 'Phòng/Ban'

    name = fields.Char(string="Tên Phòng Ban", required=True)
    employee_ids = fields.One2many('ql_nhanvien.employee', 'department_id', string="Nhân Viên")
    description = fields.Text(string="Mô Tả")
