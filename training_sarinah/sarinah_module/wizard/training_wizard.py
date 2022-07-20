from odoo import fields, models
from odoo.exceptions import ValidationError


class MultiAddAttendee(models.TransientModel):
    _name = 'multi.add.attendee.wizard'
    _description = "Multi Add Attendee"

    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    name = fields.Char(string="Name")
    phone = fields.Char(string="Phone")

    def add_attendee(self):
        # call object/class
        attendee_obj = self.env['training.attendees']
        training_obj = self.env['training.module']
        # get context
        context = dict(self._context)
        active_ids = context.get('active_ids')
        for training in training_obj.browse(active_ids):
            for attendee in self.attendee_ids:
                attendee_obj.create({
                    'attendee_id': attendee.id,
                    'training_id': training.id,
                })

    def add_attendee_single(self):
        # call object/class
        attendee_obj = self.env['training.attendees']
        training_obj = self.env['training.module']
        # get context
        context = dict(self._context)
        active_ids = context.get('active_ids')
        # check record must be one
        if len(active_ids) > 1:
            raise ValidationError("Please select one record")
        for training in training_obj.browse(active_ids):
            for attendee in self.attendee_ids:
                attendee_obj.create({
                    'attendee_id': attendee.id,
                    'training_id': training.id,
                })

    def add_attendee_partner(self):
        attendee_obj = self.env['training.attendees']
        training_obj = self.env['training.module']
        context = dict(self._context)      
        active_ids = context.get('active_ids')
        for training in training_obj.browse(active_ids):
            # create attande / partner
            attendee = self.env['res.partner'].create({'name': self.name, 'phone': self.phone})
            print(attendee)
            # create attandees on training module
            attendee_obj.create({
                'attendee_id': attendee.id,
                'training_id': training.id,
            })
