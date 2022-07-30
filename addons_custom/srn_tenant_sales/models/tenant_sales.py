from odoo import fields, models, api


class TenantSales(models.Model):
    _name = 'srn.tenant.sales'
    _description = 'Sarinah Tenant Sales'
    # naming in breadcrumb navigation form
    _rec_name = 'tenant_id'

    sales_date = fields.Date(string='Sales Date', required=True)
    day = fields.Char(string='Day')
    omzet = fields.Float(string='Omzet')
    tenant_id = fields.Many2one('res.partner', string='Tenant', required=True)
    lot_location_id = fields.Many2one(
        'product.template', string='Lot Location')
    # Untuk Production Sarinah
    # tenant_id = fields.Many2one(
    #     'res.partner', string='Tenant', domain="[('is_property', '=', True)]")
    # lot_location_id = fields.Many2one(
    #     'product.template', string='Lot Location', domain="[('is_property', '=', True)]")
    description = fields.Text(string='Description')
    brand = fields.Text(related='tenant_id.comment',
                        string='Brand', readonly=False)
    _sql_constraints = [
        ('tenant_salesdate_lot_uniq', 'unique(tenant_id, sales_date,lot_location_id)',
         'The line of Tenant, Sales Date and Lot Location must be unique'),
    ]

    @api.onchange('sales_date')
    def _get_day_name(self):
        if self.sales_date:
            self.day = self.sales_date.strftime("%A").strip()
            print(self.day)
            print(self.sales_date)
