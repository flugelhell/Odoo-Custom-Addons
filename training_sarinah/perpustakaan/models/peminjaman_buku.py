from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime


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
    total_harga_pinjam = fields.Float(
        string='Total', compute='_compute_total', store=True)
    status = fields.Selection(
        [('draft', 'Draft'), ('dipinjam', 'Dipinjam'), ('dikembalikan', 'Dikembalikan')], default='draft')

    # state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'),
    #                          ('done', 'Done')], default='draft', string="Status")
    # total_attendees = fields.Integer(string='Total Attendees')

    # trainer_id = fields.Many2one('res.users', string="Trainer")
    # assistant_ids = fields.Many2many('res.users', string="Assistant")

    # attendee_ids = fields.One2many(
    #     'training.attendees', 'training_id', string='Attendees')

    @api.depends('daftar_buku_ids')
    def _compute_total(self):
        self.total_harga_pinjam = 0
        for item in self.daftar_buku_ids:
            self.total_harga_pinjam = self.total_harga_pinjam + item.harga_pinjam_buku
            print('##################', item.harga_pinjam_buku)

    # Override saat update untuk status = dipinjam
    def write(self, vals):
        if(self.status == 'dipinjam'):
            tgl_dikembalikan = vals.get('tanggal_kembali')
            if not self.tanggal_kembali and not tgl_dikembalikan:
                raise ValidationError('Tanggal Kembali harus diisi')
            else:
                # pengecekan tanggal ada di tombol update
                return super(PeminjamanBuku, self).write(vals)
        else:
            return super(PeminjamanBuku, self).write(vals)

    def update_status(self):
        if self.status == 'draft':
            self.write({'status': 'dipinjam'})
        elif self.status == 'dipinjam':
            if self.tanggal_kembali:
                if(self.tanggal_kembali < self.tanggal_pinjam):
                    raise ValidationError(
                        'Tanggal Kembali harus diset sama dengan atau lebih besar dari Tanggal Pinjam')
                else:
                    self.write({'status': 'dikembalikan'})
            else:
                raise ValidationError("Tanggal Kembali Harus Diisi !!!")

    def update_status_to_draft(self):
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
    # Id transaksi peminjaman buku
    peminjaman_buku_id = fields.Many2one(
        'peminjaman.buku', string='Peminjam ID')
    harga_pinjam_buku = fields.Float(string='Harga Pinjam')


# class NamaClassYgDiInherit
class ProductProduct(models.Model):
    # nama model yg di inherit
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
