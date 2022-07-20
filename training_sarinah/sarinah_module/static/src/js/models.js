odoo.define('sarinah_module.models', function (require) {
    "use strict";
// odoo.define('nama_module.nama_file', function (require) {
    // "use strict";

    // get models on module pos
    var models = require('point_of_sale.models');
    // var models = require('point_of_sale.models');
    // var models = require('nama_module.nama_file');

    // SCREEN on Payment start
    // var screens = require('point_of_sale.screens');    
    // screens.PaymentScreenWidget.include({
    //     validate_order: function(force_validation) {
    //         var self = this;
    //         var subtotal = self.pos.get_order().get_subtotal()
    //         if(subtotal < 100) {
    //             self._super(event)
    //         } else {
    //            this.pos.gui.show_popup('error', {
    //                 'title': _t("Rounding error in payment lines"),
    //                 'body': _t("The amount of your payment lines must be rounded to validate the transaction."),
    //             });
    //         }
    //     },
    // });
    // finish

    // inherit models
    var orderline_super = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        initialize: function(attr,options) {
            orderline_super.initialize.apply(this,arguments);
            var lines = options.order.orderlines.models;
            for(var i = 0; i < lines.length; i++){
                if (lines[i].price < this.price){
                    lines[i].set_discount(100);
                } else {
                    this.set_discount(100);
                }
            }
        },
    });
});
