# library default
from odoo import models, fields, api
# library warning
from odoo.exceptions import ValidationError
from odoo.http import request


# class GANTINAMACLASS(models.Model):
#     _name = 'ganti.nama.model'
#     _description = 'Ganti Nama Model'

class TrainingCourse(models.Model):
    _name = 'training.module'
    _description = 'Training Course'
    _order = 'date'

    def _get_name(self):
        return "Nama"
        # return fields.Date.today()

    def _get_date(self):
        return fields.Date.today()

    def _get_number(self):
        return self.env['ir.sequence'].next_by_code('training.sequence')
        # return self.env['sale.order'].next_by_code('training.sequence')

    # masukin glosary type data

    date = fields.Date(string='Training Date', default=_get_date)
    date_time = fields.Datetime(string='Training Date time')
    training_number = fields.Char(string='Number', readonly=True, default=_get_number)
    name = fields.Char(string='Name', default=_get_name)
    registration_amount = fields.Float(string='Registration Amount')
    description = fields.Text(string='description')
    state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'), ('done', 'Done')], string="Status", default='draft')
    phone = fields.Char(string="Phone")
    trainer_id = fields.Many2one('res.users', string="Trainer")
    assistant_ids = fields.Many2many('res.users', string="Assistant")
    group_id = fields.Many2one('res.groups', string="Groups")
    csv_file = fields.Binary('File')
    # trigger
    attendee_ids = fields.One2many('training.attendees', 'training_id', string='Attendees')

    # compute
    total_attendees = fields.Integer(string='Total Attendees', compute='_compute_total', store=True)
    total_attendees_presence = fields.Integer(string='Total Attendees Presence', compute='_compute_total_presence')
    # bikin field integer dengan compute, fungsinya untuk menampilkan yang tidak hadir

    total_not_presence = fields.Integer(string='Total Attendees Not Presence', compute='_compute_total_presence')


    @api.depends('attendee_ids')
    def _compute_total(self):
        for item in self:
            item.total_attendees = len(item.attendee_ids)

    @api.depends('attendee_ids.presence')
    def _compute_total_presence(self):
        for item in self:
            # attandees
            total_attendees = len(item.attendee_ids)
            attendees = item.attendee_ids.filtered(lambda a: a.presence)
            # filter not precense
            not_attendees = total_attendees - len(attendees)
            item.total_not_presence = not_attendees
            # set value
            item.total_attendees_presence = len(attendees)
            # not_attendees = item.attendee_ids.filtered(lambda a: not a.presence)
            # item.total_not_presence = len(not_attendees)

    def update_state(self):
        if self.state == 'draft':
            self.write({'state': 'inprogress'})

    # onchange
    @api.onchange('trainer_id')
    def _onchange_trainer_id(self):
        if self.trainer_id:
            self.phone = self.trainer_id.phone

    # @api.onchange('phone')
    # def _onchange_phone(self):
    #     if self.phone and not self.trainer_id:
    #         self.trainer_id.phone = self.phone

    _sql_constraints = [
        ('training_unique', 'UNIQUE(name)', 'A name must  be unique!'),
    ]

    @api.constrains('registration_amount')
    def _check_registration_amount(self):
        if self.registration_amount <= 0:
            raise ValidationError('Registration amount must be greater than zero')

    # action pemanggilan button
    def action_create_multi_attandee(self):
        view = self.env.ref('sarinah_module.wizard_training_view')
        return {
            'name': ('Create Attandee'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'multi.add.attendee.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': self.env.context,
        }

    def action_create_partner(self):
        view = self.env.ref('sarinah_module.wizard_training_view_partner')
        return {
            'name': ('Create Attandee'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'multi.add.attendee.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': self.env.context,
        }

    # @api.model
    def write(self, vals):
        # super default
        res = super(TrainingCourse, self).write(vals)
        print("**** WRITE ****")
        print(res)
        print(vals)
        if vals.get('phone'):
            self.trainer_id.write({'phone': vals.get('phone')})
        return res


class TrainingAttendees(models.Model):
    _name = 'training.attendees'
    _description = 'Training Attendees'

    attendee_id = fields.Many2one('res.partner', string='Attendee')
    presence = fields.Boolean(string='Presence')
    training_id = fields.Many2one('training.module', string='Training')
    phone = fields.Char(related="attendee_id.phone", string="Phone")
    is_select = fields.Boolean("Select")
    sequence = fields.Integer(string='Sequence', default=10)


class ResUsers(models.Model):
    _inherit = 'res.users'

    training_ids = fields.Many2many(
        'training.module', compute='_compute_training', string='Training')
    
    user_sales = fields.Boolean(string="POS operator")

    def _compute_training(self):
        # ke objeck training.module
        training_obj = self.env['training.module']
        print("XXXXXXXXXXXXXXXXX")
        # search record dengan kondisi
        training = training_obj.search([('trainer_id', '=', self.id)])
        self.training_ids = training.ids

class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        res = super(Http, self).session_info()
        res['user_sales'] = request.env.user.user_sales
        return res
