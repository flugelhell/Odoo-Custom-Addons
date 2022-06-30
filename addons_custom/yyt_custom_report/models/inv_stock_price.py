# Reporting untuk menampilkan stock dan price
from odoo import api, fields, models, tools


class YytInvStockPrice(models.Model):
    _name = 'yyt.inv_stock_price'
    _description = 'Inventory Stock Price'
    _auto = False  # don't create any database backend

    id = fields.Many2one(
        string='Product Id', comodel_name='product.product')
    owner = fields.Char(string='Owner')
    brand = fields.Char(string='Brand')
    consignment = fields.Char(string='Consignment')
    sku = fields.Char(string='SKU')
    barcode = fields.Char(string='Barcode')
    name = fields.Char(string='Product Name')
    variant = fields.Char(string='Product Variant',
                          help='Only show variant size and warna/jenis')
    qoh = fields.Integer(string='QOH')
    price = fields.Integer(string='Price')
    location = fields.Char(string='Location')
    pricelist = fields.Char(string='Pricelist')
    active = fields.Boolean(string='Active')

    def init(self):
        cr = self.env.cr
        tools.drop_view_if_exists(cr, 'yyt_inv_stock_price')
        cr.execute("""
        CREATE OR REPLACE VIEW yyt_inv_stock_price AS 
        (
            SELECT prod.id AS id,
            COALESCE(partner.name, ''::character varying) AS owner,
            COALESCE(brand.name, ''::character varying) AS brand,
            CASE
                WHEN (prodtmpl.is_consignment = true) THEN 'BKS'::text
                ELSE 'BS'::text
            END AS consignment,
            prod.default_code AS sku,
            prod.barcode,
            prodtmpl.name AS name,
            ( SELECT string_agg((pav.name)::text, ', '::text ORDER BY pav.attribute_id) AS attribute_names
                FROM (product_attribute_value pav
                    LEFT JOIN product_template_attribute_value ptav ON ((ptav.product_attribute_value_id = pav.id)))
                WHERE ((ptav.id IN ( SELECT (unnest(string_to_array((product_product.combination_indices)::text, ','::text)))::integer AS unnest
                        FROM product_product
                        WHERE (product_product.id = prod.id))) AND ((pav.attribute_id = 1) OR (pav.attribute_id = 5)))) AS variant,
            sum(sq.quantity) AS qoh,
            COALESCE(round(( SELECT product_pricelist_item.fixed_price
                FROM product_pricelist_item
                WHERE (product_pricelist_item.id = ( SELECT max(product_pricelist_item_1.id) AS max
                        FROM product_pricelist_item product_pricelist_item_1
                        WHERE ((product_pricelist_item_1.product_id = prod.id) AND (product_pricelist_item_1.pricelist_id = vl.pricelist_id) AND (product_pricelist_item_1.active = true))))), 0), (0)::numeric) AS price,
            vl.name AS location,
            ( SELECT product_pricelist.name
                FROM product_pricelist
                WHERE (product_pricelist.id = vl.pricelist_id)) AS pricelist,
            prod.active as active
            FROM (((((vendor_location vl
                LEFT JOIN stock_quant sq ON ((sq.location_id = vl.location_id)))
                LEFT JOIN product_product prod ON ((prod.id = sq.product_id)))
                LEFT JOIN product_template prodtmpl ON ((prodtmpl.id = prod.product_tmpl_id)))
                LEFT JOIN res_partner partner ON ((partner.id = prodtmpl.owner_id)))
                LEFT JOIN product_brand brand ON ((brand.id = prodtmpl.brand_id)))
            WHERE (vl.active = true)
            GROUP BY prod.id, prodtmpl.name, vl.name, vl.pricelist_id, partner.name, brand.name, prodtmpl.is_consignment
            ORDER BY vl.name, partner.name, brand.name
        )
        """)
