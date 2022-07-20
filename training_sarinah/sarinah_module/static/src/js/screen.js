odoo.define('training.screens', function (require) {
    "use strict";

    var session = require('web.session');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var _t = core._t;

    var current_id = session.uid
    // file models on screens.namemodel(namaclass).include
    screens.PaymentScreenWidget.include({
        validate_order: function(force_validation) {
            var self = this;
            console.log("****POS****")
            console.log(self)
            // function to get subtotal order
            var subtotal = self.pos.get_order().get_subtotal()
            if(subtotal < 100) {
                // super func to method odoo
                self._super(event)
            } else {
               this.pos.gui.show_popup('error', {
                    'title': _t("Rounding error in payment lines"),
                    'body': _t("The amount of your payment lines must be rounded to validate the transaction."),
                });
            }
        },
    });
});
    