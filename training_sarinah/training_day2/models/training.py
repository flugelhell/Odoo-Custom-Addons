from odoo import models, fields, api
from odoo.exceptions import ValidationError


list_state = [
    ('draft', 'Draft'),
    ('inprogress', 'In progress'),
    ('done', 'Done')
]


class TrainingCourse(models.Model):
    _name = 'training.module'
    _description = 'Training Course'

    def _get_date(self):
        return fields.Date.today()

    def _get_number(self):
        return self.env['ir.sequence'].next_by_code('inv.sequence')

    date = fields.Date(string='Training Date', default=_get_date)
    training_number = fields.Char(string='Number', readonly=True, default=_get_number)
    active = fields.Boolean(default=True, string='Active')

    name = fields.Char(string='Name')
    registration_amount = fields.Float(string='Registration Amount')
    description = fields.Text(string='description')
    state = fields.Selection(list_state, string="Status", default='draft')
    total_attendees = fields.Integer(string='Total Attendees', compute='_compute_total')
    # new field
    total_not_attendees = fields.Integer(string='Total Not Attendees', compute='_compute_total_presence')
    total_attendees_presence = fields.Integer(string='Total Attendees Presence', compute='_compute_total_presence')
    phone = fields.Char(string="Phone")
    trainer_id = fields.Many2one('res.users', string="Trainer")
    assistant_ids = fields.Many2many('res.users', string="Assistant")
    attendee_ids = fields.One2many('training.attendees', 'training_id', string='Attendees')
    csv_file = fields.Binary('File')

    @api.model
    def create(self, vals):
        if 'name' in vals:
            vals['name'] = vals.get('name').upper()
        res = super(TrainingCourse, self).create(vals)
        return res



    def update_state(self):
        if self.state == 'draft':
            self.write({'state': 'inprogress'})
        elif self.state == 'inprogress':
            self.write({'state': 'done'})
        else:
            self.write({'state': 'draft'})

    @api.depends('attendee_ids')
    def _compute_total(self):
        for item in self:
            item.total_attendees = len(item.attendee_ids)

    @api.depends('attendee_ids.presence')
    def _compute_total_presence(self):
        for item in self:
            print("COMPUTE")
            print(item)
            print("VARIABLE")
            print(item.attendee_ids)
            # kecentang
            attendees = item.attendee_ids.filtered(lambda a: a.presence)
            print(attendees)
            item.total_attendees_presence = len(attendees)
            # ga kecentanf
            not_attandees = item.attendee_ids.filtered(lambda a: not a.presence)
            item.total_not_attendees = len(not_attandees)

    @api.onchange('trainer_id')
    def _onchange_trainer_id(self):
        print("XXXXXXXXXXXXXXXXXXX")
        if self.trainer_id:
            self.phone = self.trainer_id.phone

    # @api.onchange('trainer_id')
    def _onchange_date(self):
        return fields.Date.today()

    _sql_constraints = [
        ('training_unique', 'UNIQUE(name)', 'A name must be unique!'),
    ]

    @api.constrains('registration_amount')
    def _check_registration_amount(self):
        if self.registration_amount <= 0:
            raise ValidationError('Registration amount must be greater than zero')

    @api.constrains('date')
    def _check_date(self):
        if self.date < fields.Date.today():
            raise ValidationError('Tidak boleh backdate')


class TrainingAttendees(models.Model):
    _name = 'training.attendees'
    _description = 'Training Attendees'

    attendee_id = fields.Many2one('res.partner', string='Attendee')
    presence = fields.Boolean(string='Presence')
    training_id = fields.Many2one('training.module', string='Training')
    phone = fields.Char(related="attendee_id.phone", string="Phone")


class ResUsers(models.Model):
    _inherit = 'res.users'

    training_ids = fields.Many2many(
        'training.module', string='Training', compute="_compute_training")

    def _compute_training(self):
        training_obj = self.env['training.module']
        training = training_obj.search([('trainer_id', '=', self.id)])
        self.training_ids = training.ids
