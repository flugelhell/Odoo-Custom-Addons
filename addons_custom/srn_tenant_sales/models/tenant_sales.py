from odoo import fields, models, api


class TenantSales(models.Model):
    _name = 'srn.tenant.sales'
    _description = 'Sarinah Tenant Sales'

    sales_date = fields.Date(string='Sales Date')
    day = fields.Char(string='Day')
    omzet = fields.Float(string='Omzet')
    tenant_id = fields.Many2one('res.partner', string='Tenant')
    lot_location_id = fields.Many2one(
        'product.template', string='Lot Location')
    # Untuk Production Sarinah
    # tenant_id = fields.Many2one(
    #     'res.partner', string='Tenant', domain="[('is_property', '=', True)]")
    # lot_location_id = fields.Many2one(
    #     'product.template', string='Lot Location', domain="[('is_property', '=', True)]")
    description = fields.Text(string='Description')

    @api.onchange('sales_date')
    def _get_day_name(self):
        if self.sales_date:
            self.day = self.sales_date.strftime("%A").strip()
            print(self.day)
            print(self.sales_date)
