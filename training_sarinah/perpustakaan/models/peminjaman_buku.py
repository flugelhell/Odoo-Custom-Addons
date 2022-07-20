from odoo import fields, models


class PeminjamanBuka(models.Model):
    _name = 'peminjaman.buku'
    _description = 'Module Perpustakan'

    name = fields.Char(string='Name')
    tanggal_pinjam = fields.Date(string='Tanggal Pinjam')
    tanggal_kembali = fields.Date(string='Tanggal Kembali')
    peminjam_id = fields.Many2one('res.users', string='Peminjam')
    no_telp = fields.Char(string='No Telp')
    petugas_id = fields.Many2one('res.users', string='Petugas')
    daftar_buku_ids = fields.One2many(
        'daftar.buku', 'peminjaman_buku_id', string='Daftar Buku')
    total_harga_pinjam = fields.Float(string='Total Harga Pinjam')
    status = fields.Selection(
        [('dipinjam', 'Dipinjam'), ('dikembalikan', 'Dikembalikan')])

    # state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'),
    #                          ('done', 'Done')], default='draft', string="Status")
    # total_attendees = fields.Integer(string='Total Attendees')

    # trainer_id = fields.Many2one('res.users', string="Trainer")
    # assistant_ids = fields.Many2many('res.users', string="Assistant")

    # attendee_ids = fields.One2many(
    #     'training.attendees', 'training_id', string='Attendees')


class DaftarBuku(models.Model):
    _name = 'daftar.buku'
    _description = 'Daftar Buku'

    buku_id = fields.Many2one('product.product', string='Buku')
    nama_buku = fields.Char(related='buku_id.name', string='Nama Buku')
    peminjaman_buku_id = fields.Many2one(
        'peminjaman.buku', string='Peminjam ID')
    harga_pinjam_buku = fields.Float(string='Harga Pinjam')


# Menambahkan Field di product.product (ProductProduct dilihat dari module product odoo di bagian Model)
class ProductProduct(models.Model):
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
