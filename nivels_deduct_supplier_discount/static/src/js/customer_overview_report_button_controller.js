odoo.define('nivels_sams_mis.CustomerOverviewReportController', function (require) {
"use strict";

var core = require('web.core');
var ListController = require('web.ListController');

var _t = core._t;
var qweb = core.qweb;

ListController.include({
    events: _.extend({
        'click .o_button_refresh_customer_overview_report': '_refreshCustomerOverciewReport'
    }, ListController.prototype.events),
    /**
     * @override
     */
    init: function (parent, model, renderer, params) {
        if (this.modelName === "customer.overview.report") {
            this._refreshCustomerOverciewReport()
        }
        return this._super.apply(this, arguments);
    },

    // -------------------------------------------------------------------------
    // Public
    // -------------------------------------------------------------------------

    /**
     * @override
     */
    renderButtons: function ($node) {
        this._super.apply(this, arguments);
        if (this.modelName === "customer.overview.report") {
            var $validationButton = $(qweb.render('CustomerOverview.Buttons'));
            this.$buttons.prepend($validationButton);
            this.$buttons.find('.o_list_button_add').hide()
        }

    },

    // -------------------------------------------------------------------------
    // Handlers
    // -------------------------------------------------------------------------

    _refreshCustomerOverciewReport: function () {
        var self = this;
        var prom = Promise.resolve();

        prom.then(function () {
            self._rpc({
                model: 'customer.overview.report',
                method: 'customer_overview_report',
                args: [[]]
            }).then(function (res) {
                self.reload();
            });
        });
    },
});

});
