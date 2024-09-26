from odoo import models, fields

class Role(models.Model):
    _name = 'ql_nhanvien.role'
    _description = 'Vị trí'

    name = fields.Char(string="Tên Vị trí", required=True)
    description = fields.Text(string="Mô Tả vị trí công việc")
    employee_ids = fields.Many2many('ql_nhanvien.employee', string="Nhân Viên")
