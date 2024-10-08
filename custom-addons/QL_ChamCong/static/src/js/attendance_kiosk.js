odoo.define('QL_ChamCong.kiosk_mode', ['web.core', 'web.AbstractAction'], function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var QWeb = core.qweb;

    var KioskMode = AbstractAction.extend({
        template: 'QL_ChamCong.KioskModeTemplate',
        events: {
            'click .o_hr_attendance_button_kiosk': '_onClickKioskButton',
        },

        /**
         * Khởi tạo
         */
        init: function (parent, context) {
            this._super.apply(this, arguments);
            this.use_camera = context.use_camera || false;
        },

        /**
         * Hàm bắt đầu chế độ Kiosk Mode
         */
        start: function () {
            this._super.apply(this, arguments);
            if (this.use_camera) {
                this._activateCamera();
            }
        },

        /**
         * Kích hoạt camera
         */
        _activateCamera: function () {
            console.log("Camera activated for Kiosk Mode!");
        },

        /**
         * Hàm xử lý sự kiện khi click vào nút chấm công
         */
        _onClickKioskButton: function () {
            console.log("Employee checked in using Kiosk Mode!");
        },
    });

    core.action_registry.add('ql_nhanvien_attendance_kiosk_mode', KioskMode);

    return KioskMode;
});
