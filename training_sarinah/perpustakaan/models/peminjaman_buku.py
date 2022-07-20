from odoo import fields, models, api


class PeminjamanBuku(models.Model):
    _name = 'peminjaman.buku'
    _description = 'Module Perpustakan'

    name = fields.Char(string='Name', readonly=True,
                       required=True, copy=False, default='New')
    tanggal_pinjam = fields.Date(string='Tanggal Pinjam', required=True)
    tanggal_kembali = fields.Date(string='Tanggal Kembali')
    peminjam_id = fields.Many2one(
        'res.users', string='Peminjam', required=True)
    no_telp = fields.Char(string='No Telp')
    petugas_id = fields.Many2one('res.users', string='Petugas')
    daftar_buku_ids = fields.One2many(
        'daftar.buku', 'peminjaman_buku_id', string='Daftar Buku')
    total_harga_pinjam = fields.Float(string='Total Harga Pinjam')
    status = fields.Selection(
        [('draft', 'Draft'), ('dipinjam', 'Dipinjam'), ('dikembalikan', 'Dikembalikan')], default='draft')

    # state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'),
    #                          ('done', 'Done')], default='draft', string="Status")
    # total_attendees = fields.Integer(string='Total Attendees')

    # trainer_id = fields.Many2one('res.users', string="Trainer")
    # assistant_ids = fields.Many2many('res.users', string="Assistant")

    # attendee_ids = fields.One2many(
    #     'training.attendees', 'training_id', string='Attendees')
    def update_status(self):
        if self.status == 'draft':
            self.write({'status': 'dipinjam'})
        elif self.status == 'dipinjam':
            self.write({'status': 'dikembalikan'})
        else:
            self.write({'status': 'draft'})

    # Membuat sequence, harus membuat record xml juga
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'pinjam.buku.sequence') or 'New'
        result = super(PeminjamanBuku, self).create(vals)
        return result


class DaftarBuku(models.Model):
    _name = 'daftar.buku'
    _description = 'Daftar Buku'

    buku_id = fields.Many2one('product.product', string='Buku')
    peminjaman_buku_id = fields.Many2one(
        'peminjaman.buku', string='Peminjam ID')
    harga_pinjam_buku = fields.Float(string='Harga Pinjam')


# Menambahkan Field di product.product (Product dilihat dari module product odoo di bagian Model)
class Product(models.Model):
    _inherit = 'product.product'

    sinopsis = fields.Text(string='Sinopsis')


# class TrainingAttendees(models.Model):
#     _name = 'training.attendees'
#     _description = 'Training Attendees'

#     attendee_id = fields.Many2one('res.partner', string='Attendee')
#     presence = fields.Boolean(string='Presence')
#     training_id = fields.Many2one('training.module', string='Training')
#     phone = fields.Char(related="attendee_id.phone", string="Phone")


# class ResUsers(models.Model):
#     _inherit = 'res.userss'

#     training_ids = fields.Many2many(
#         'training.module', string='Training')
