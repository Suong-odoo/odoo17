from odoo import models, fields, api

class AttendanceKiosk(models.Model):
    _inherit = 'ql_nhanvien.attendance'

    def action_activate_camera(self):
        """
        Kích hoạt camera để quét mã QR
        """
        # Hàm giả lập để xử lý camera (chỉ dùng minh họa)
        if self.use_camera:
            # Logic kích hoạt camera
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Camera đã được kích hoạt!',
                    'type': 'rainbow_man',
                }
            }
