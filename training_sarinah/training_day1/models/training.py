from odoo import fields, models


class TrainingCourse(models.Model):
    _name = 'training.module'
    _description = 'Training Course'

    name = fields.Char(string='Name')
    registration_amount = fields.Float(string='Registration Amount')
    date = fields.Date(string='Training Date')
    description = fields.Text(string='description')
    state = fields.Selection([('draft', 'Draft'), ('inprogress', 'In progress'), ('done', 'Done')], default='draft' , string="Status")
    total_attendees = fields.Integer(string='Total Attendees')

    trainer_id = fields.Many2one('res.users', string="Trainer")
    assistant_ids = fields.Many2many('res.users', string="Assistant")

    attendee_ids = fields.One2many('training.attendees', 'training_id', string='Attendees')


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
        'training.module', string='Training')
