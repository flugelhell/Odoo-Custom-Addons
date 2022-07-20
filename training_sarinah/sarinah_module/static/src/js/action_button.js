odoo.define('training.ActionButton', function (require) {
    "use strict";

    var session = require('web.session');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var _t = core._t;

    var current_id = session.uid
    
    screens.ActionpadWidget.include({
        renderElement: function() {
            var self = this;
            this._super();
            this.$('.pay').click(function(){
                var subtotal = self.pos.get_order().get_subtotal()
                var sales = session.user_sales
                if(subtotal != 0){
                    self.gui.show_popup('confirm',{
                        'title': _t('Validation'),
                        'body':  _t('Please confirm or cancel your payment'),
                        confirm: function(){
                            self.gui.show_popup('confirm',{
                                'title': _t('Validation'),
                                'body':  _t('Apakah Anda Yakin'),
                                confirm: function(){
                                    return self.gui.show_screen('payment');
                                },
                                cancel: function(){
                                    return self.gui.show_screen('products');
                                },
                            });
                            // return self.gui.show_screen('payment');
                        },
                        cancel: function(){
                            self.gui.show_popup('confirm',{
                                'title': _t('Validation'),
                                'body':  _t('Apakah Anda Yakin ingin batal'),
                                confirm: function(){
                                    return self.pos.delete_current_order();
                                },
                                cancel: function(){
                                    return self.gui.show_screen('payment');
                                },
                            });
                            // return self.gui.show_screen('products');
                        },
                    });
                }
            });
        },
    });
});
    