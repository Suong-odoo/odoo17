from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import AccessError

class ResUsers(models.Model):
    _inherit = 'res.users'
    employee_ids = fields.One2many('ql_nhanvien.employee', 'user_id', string='Nhân viên liên kết')
    employee_id = fields.Many2one('ql_nhanvien.employee', string="Nhân viên Công ty",
                                  compute='_compute_company_employee', search='_search_company_employee', store=False)
    @api.depends('employee_ids')
    @api.depends_context('company')
    def _compute_company_employee(self):
        employee_per_user = {
            employee.user_id: employee
            for employee in self.env['ql_nhanvien.employee'].search([('user_id', 'in', self.ids), ('company_id', '=', self.env.company.id)])
        }
        for user in self:
            user.employee_id = employee_per_user.get(user)

    def _search_company_employee(self, operator, value):
        return [('employee_ids', operator, value)]

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        employee_create_vals = []
        for user, vals in zip(res, vals_list):
            if vals.get('create_employee_id'):
                self.env['ql_nhanvien.employee'].browse(vals.get('create_employee_id')).user_id = user
            else:
                employee_create_vals.append({
                    'name': user.name,
                    'user_id': user.id,
                })
        if employee_create_vals:
            self.env['ql_nhanvien.employee'].create(employee_create_vals)
        return res

    def write(self, vals):
        result = super(ResUsers, self).write(vals)
        employee_values = {fname: vals[fname] for fname in ['name', 'email'] if fname in vals}
        if employee_values:
            employees = self.env['ql_nhanvien.employee'].sudo().search([('user_id', 'in', self.ids)])
            employees.write(employee_values)
        return result
