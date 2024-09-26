odoo.define('QL_NhanVien.QRScanner', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');

    var QRScanner = Widget.extend({
        template: 'QRScannerTemplate',
        events: {
            'click .start-scan': '_startScan',
        },

        willStart: function () {
            return this._super.apply(this, arguments);
        },

        start: function () {
            return this._super.apply(this, arguments);
        },

        _startScan: function () {
            navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
            .then((stream) => {
                this.$('.qr-video')[0].srcObject = stream;
                this._scanQRCode();
            }).catch(console.error);
        },

        _scanQRCode: function () {
            var video = this.$('.qr-video')[0];
            var canvasElement = this.$('.qr-canvas')[0];
            var canvas = canvasElement.getContext('2d');

            // Quét mã QR liên tục từ video stream
            var scanningInterval = setInterval(() => {
                if (video.readyState === video.HAVE_ENOUGH_DATA) {
                    canvasElement.height = video.videoHeight;
                    canvasElement.width = video.videoWidth;
                    canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);
                    var imageData = canvas.getImageData(0, 0, canvasElement.width, canvasElement.height);
                    var code = jsQR(imageData.data, imageData.width, imageData.height, {
                        inversionAttempts: "dontInvert",
                    });

                    if (code) {
                        clearInterval(scanningInterval);
                        console.log("Found QR code", code.data);
                        // Xử lý dữ liệu mã QR tại đây
                    }
                }
            }, 100);
        },
    });

    core.action_registry.add('qr_scanner', QRScanner);

    return QRScanner;
});

