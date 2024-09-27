from odoo import models, fields, api

class CompanyInfo(models.Model):
    _name = 'ql_nhanvien.company'
    _description = 'Thông tin công ty'

    name = fields.Char(string="Tên công ty", required=True)
    logo = fields.Binary(string="Logo Công ty", attachment=True)
    address = fields.Char(string="Địa chỉ")
    phone = fields.Char(string="Số điện thoại")
    mobile = fields.Char(string="Số di động")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")
    tax_id = fields.Char(string="Mã số thuế")
    tags = fields.Char(string="Tags")
