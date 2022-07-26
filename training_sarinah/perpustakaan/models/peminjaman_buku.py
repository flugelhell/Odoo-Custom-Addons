from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Header Table


class PeminjamanBuku(models.Model):
    _name = 'peminjaman.buku'
    _description = 'Module Perpustakan'

    def _current_date():
        return datetime.today().date()

    name = fields.Char(string='Name', readonly=True,
                       required=True, copy=False, default='New')
    tanggal_pinjam = fields.Date(
        string='Tanggal Pinjam', required=True, default=_current_date())
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

    @api.onchange('tanggal_pinjam')
    def _onchange_tanggal_pinjam(self):
        if self.tanggal_pinjam:
            self.tanggal_kembali = self.tanggal_pinjam + relativedelta(weeks=1)

    @api.depends('daftar_buku_ids')
    def _compute_total(self):
        # Cara 1
        # self.total_harga_pinjam = 0
        # for item in self.daftar_buku_ids:
        #     self.total_harga_pinjam = self.total_harga_pinjam + item.harga_pinjam_buku
        #     print('##################', item.harga_pinjam_buku)
        # Cara 2
        self.total_harga_pinjam = sum(
            [line.harga_pinjam_buku for line in self.daftar_buku_ids])

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

# detail table


class DaftarBuku(models.Model):
    _name = 'daftar.buku'
    _description = 'Daftar Buku'

    buku_id = fields.Many2one('product.product', string='Buku')
    # Id transaksi peminjaman buku
    peminjaman_buku_id = fields.Many2one(
        'peminjaman.buku', string='Peminjam ID')
    harga_pinjam_buku = fields.Float(string='Harga Pinjam')
    # ambil data dari product.product via related, field ini tidak akan terbentuk kolom di table
    sinopsis = fields.Text(related='buku_id.sinopsis', string='Sinopsis')


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
