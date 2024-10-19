from odoo import fields, models, api
import logging

class InstallationEvent(models.Model):
    _name = 'installation.event'
    _description = 'A calendar event of a selfconsumption installation'

    name = fields.Char(
        string='name')
    installation_id = fields.Many2one(
        comodel_name='selfconsumption.installation',
        string='Installation',
        ondelete='cascade')
    start_date = fields.Datetime(
        string='Start date')
    end_date = fields.Datetime(
        string='End date')
    type = fields.Selection(
        [
            ('replanteo', 'Replanteo'),
            ('obra', 'Obra'),
            ('requerimiento', 'Requerimiento')
        ],
        string='Type')

    requierement_ids = fields.One2many(
        comodel_name='installation.legal.requirement',
        inverse_name='installation_event_id',
        invisible=True
    )


    def write(self, vals):
        res = super().write(vals)
        if self.installation_id:
            installation = self.env['selfconsumption.installation'].browse([self.installation_id.id])
            if self.type == 'replanteo' and installation.stake_out_date != self.start_date:
                installation.write({'stake_out_date': self.start_date})
            elif self.type == 'obra' and (installation.construction_start_date != fields.Date.to_date(self.start_date) or installation.construction_end_date != fields.Date.to_date(self.end_date)):
                installation.write({'construction_start_date': fields.Date.to_date(self.start_date), 'construction_end_date': fields.Date.to_date(self.end_date)})
            elif self.type == 'replanteo':
                for requirement in self.requierement_ids:
                    if (requirement.limit_date != fields.Date.to_date(self.start_date)):
                        requirement.limit_date = fields.Date.to_date(self.start_date)
        return res

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.installation_id:
            installation = self.env['selfconsumption.installation'].browse([res.installation_id.id])
            if res.type == 'replanteo' and not installation.stake_out_date:
                installation.write({'stake_out_date': res.start_date})
            elif res.type == 'obra' and (not installation.construction_start_date or not installation.construction_end_date):
                installation.write({'construction_start_date': fields.Date.to_date(res.start_date), 'construction_end_date': fields.Date.to_date(res.end_date)})
        return res

    def unlink(self):
        for event in self:
            events = self.env['installation.event'].search([('installation_id', '=', event.installation_id.id),('type', '=', event.type), ('id', '!=', event.id)])
            requierements = event.requierement_ids
            event_type = event.type
            installation = event.installation_id
            super(InstallationEvent, event).unlink()
            if not events:
                if event_type == 'obra':
                    installation.write({'construction_start_date': None, 'construction_end_date': None})
                elif event_type == 'replanteo':
                    installation.write({'stake_out_date': None})