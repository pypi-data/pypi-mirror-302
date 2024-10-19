from odoo import api, fields, models
import logging

class SelfconsumptionInstallation(models.Model):
    _name = 'selfconsumption.installation'

    name = fields.Char(string="Name")

    status = fields.Selection([
        ("active", "Active"),
        ("deactivated", "Deactivated"),
        ("executed", "executed"),
        ("in-service", "In service"),
    ], string="Status", tracking=True)

    project = fields.Many2one(
        comodel_name="project.project",
        string="Project"
    )

    partner_id = fields.Many2one('res.partner', string='Customer', auto_join=True, tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    # Proyecto
    code = fields.Char(string="Código")
    
    installer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Instalador',
        domain="[('supplier_rank','>', 1)]")

    installer_tag = fields.Many2one( #Recuired computed field to allow filtering by config value in domain
        comodel_name='res.partner.category',
        compute='_compute_installer_tag',
        store=False
    )

    surge = fields.Selection([
        ('o3', 'O3'),
        ('lre', 'LRE'),
        ('ims', 'IMS'),
        ('org', 'ORG'),
        ('eru', 'ERU'),
        ('col', 'COL'),
        ],
        string='Oleada')
    activation_date = fields.Date(
        string='Fecha activación')
    lead_code = fields.Char(
        string="Código lead")

    project_phase = fields.Char(
        string='Fase proyecto')

    typology = fields.Selection([
            ('individual', 'Individual'),
            ('collective', 'Collective')
        ],
        string="Typology"
    )

    subgroup = fields.Char(
        string="Subgroup")

    model_shortlisted = fields.Char(
        string='Modelo preelegido')

    power_shortlisted = fields.Integer(
        string='Potencia preelegida (kW)')

    notes_shortlisted = fields.Text(
        string='Notas proyecto')
    
    maintenance_contact = fields.Many2one(
        comodel_name='res.partner',
        string='Maintenance contact')

    # suministro
    supplier_id = fields.Many2one(
        comodel_name='res.partner',
        string='Supplier')

    supplier_tag = fields.Many2one( #Recuired computed field to allow filtering by config value in domain
        comodel_name='res.partner.category',
        compute='_compute_supplier_tag',
        store=False
    )
    partner_id2 = fields.Many2one(
        comodel_name='res.partner',
        string='Titular factura')
    partner_id2_name = fields.Char(
        string='Nombre titular')
    partner_id2_surname = fields.Char(
        string='Apellidos titular')
    partner_id2_vat = fields.Char(
        string='DNI titular')
    supply_street = fields.Char(
        string='Dirección suministro')
    supply_zip = fields.Char(
        string='CP suministro')
    supply_state= fields.Char(
        string='Supply state'
    )
    supply_region=fields.Char(
        string='Supply region'
    )
    supply_municipality=fields.Char(
        string='Supply municipality'
    )
    supply_comercial = fields.Char(
        string='Comercializadora')
    cups = fields.Char(
        string='CUPS')
    contract_power = fields.Float(
        string='Potencia contratada')
    energy_cost = fields.Float(
        string='Average energy cost €/kWh')
    fixed_toll_cost = fields.Float(
        string = 'Fixed toll cost €/Kw.day')
    annual_energy_consumed = fields.Integer(
        string='Energia consumida anual kWh/año')
    phase = fields.Selection([
        ('monophase', 'Monofásico'),
        ('threefase', 'Trifásico')],
        string='Fase')
    access_pricelist = fields.Char(
        string='Tarifa acceso')
    bill_recieved = fields.Boolean(
        string='Electric Bill Recieved'
    )


    # ubicación
    stake_out_date = fields.Datetime("Fecha de replanteo")
    installation_address = fields.Char(
        string='Dirección instalación')
    installation_zip = fields.Char(
        string='CP instalación')
    installation_city = fields.Char(
        string='Municipio instalación')
    estimated_inclination = fields.Integer("Inclinación estimada")
    cover_type_id = fields.Many2one(
        comodel_name='installation.type.cover',
        string='Tipo cubierta')
    gmaps_address = fields.Char("Dirección Gmaps")
    gmaps_link = fields.Char("Google maps link")
    catastral = fields.Char(
        string='Catastro')
    utm_coords = fields.Char(
        string='Coordenadas UTM')
    location_notes = fields.Text(
        string='Notas ubicación')
    roof_height = fields.Char(
        string = 'Roof height')
    stake_out_completed = fields.Boolean(
        string = 'Stakeout completed'
    )
    heritage_protection = fields.Boolean(
        string ='Heritage protection'
    )

    # Simulacion
    project_simulation_ids = fields.One2many(
        comodel_name='selfconsumption.installation.simulator',
        inverse_name='installation_id',
        string='Simulaciones')

    # Ejecución
    blueprint_chosen = fields.Many2one(
        comodel_name='selfconsumption.installation.simulator',
        string='Anteproyecto elegido')
    rated_power_execution = fields.Float(
        string='Potencia nominal (W)',
        compute='_compute_rated_power',
        store=True)
    peak_power_execution = fields.Float(
        string='Potencia pico (W)',
        compute='_compute_peak_power',
        store=True)
    cover_type_execution_id = fields.Many2one(
        comodel_name='installation.type.cover',
        string='Tipo cubierta')
    anchorage_type = fields.Many2one(
        comodel_name='installation.type.anchorage',
        string='Tipo anclaje')
    structure_type = fields.Many2one(
        comodel_name='installation.type.structure',
        string='Tipo estructura')
    structure_inclination=fields.Char(
        string='Structure inclination'
    )
    structure_orientation=fields.Char(
        string='Structure orientation'
    )
    cover_extra_info=fields.Char(
        string='Others'
    )
    structure=fields.Char(
        string='Structure model'
    )
    civil_construction = fields.Char(
        string='Obra civil')
    media_aux = fields.Char(
        string='Medios auxiliares')
    extra_element_1 = fields.Char(
        string='Elemento extra 1')
    extra_element_2 = fields.Char(
        string='Elemento extra 2')
    extra_element_3 = fields.Char(
        string='Elemento extra 3')
    design_notes = fields.Text(
        string='Notas diseño')
    construction_start_date = fields.Date(
        string='Fecha inicio obra')
    construction_end_date = fields.Date(
        string='Fecha fin obra')
    construction_address = fields.Char(
        string='Construction address'
    )
    execution_date = fields.Char(
        string='Execution date'
    )
    mains_voltage=fields.Char(
        string='Mains voltage'
    )
    gcp_location=fields.Char(
        string='GCP Location'
    )
    gcp_fuse_rated_current=fields.Float(
        string='Fuse rated current'
    )
    gcp_lga_section=fields.Float(
        string='LGA section'
    )
    gcp_fuseholder_type=fields.Char(
        string='Fuseholder type'
    )
    gcp_general_switch=fields.Char(
        string='General Switch'
    )
    dc_safety_fuse=fields.Char(
        string='DC Safety fuse'
    )
    dc_fuseholder_type=fields.Char(
        string='DC fuseholder type'
    )
    pv_line_meter_type=fields.Char(
        string='Meter type'
    )
    pv_line_meter_sn=fields.Char(
        string='Meter serial number'
    )
    pv_safety_fuse=fields.Char(
        string='PV Safety fuse'
    )
    pv_disconectors=fields.Char(
        string='PV disconectors'
    )
    pv_registrar_number=fields.Char(
        string='Registrar number'
    )

    nature_of_supply=fields.Char(
        string='Nature of supply'
    )
    new_or_expansion=fields.Selection([
        ('new', 'New'), ('expansion','Expansion')],
        string='New or expansion'
    )
    line_ids = fields.One2many(
        comodel_name='installation.electric.line',
        inverse_name='installation_id',
        string='Electric lines')

    inverter_ids = fields.One2many(
        comodel_name='installation.inverter',
        inverse_name='installation_id',
        string='Inverters')
    
    module_ids = fields.One2many(
        comodel_name='installation.module',
        inverse_name='installation_id',
        string='Modules')
    cnmc_connection_type = fields.Char(
        string='CNMC Connection type'
    )
    installation_typology_execution=fields.Char(
        string='Installation typology'
    )
    monitorization_email=fields.Char(
        string='Email'
    )
    monitorization_password=fields.Char(
        string='Password'
    )
    monitorization_public_link=fields.Char(
        string='Public link'
    )
    zero_injection=fields.Boolean(
        string='0 Injection'
    )
    supply_connection=fields.Selection([
            ('BT', 'BT'),
            ('AT', 'AT')
        ],
        string='Supply connection'
    )



    week_construction = fields.Integer(
        string='Semana de obra',
        compute='_compute_construction_week',
        store=True)
    investor_serial_number = fields.Char(
        string='Número de serie del inversor')

    # Licencia/Ayuntamiento
    license_type = fields.Char(
        string='Tipo permiso')
    requested_by = fields.Char(
        string='Solicitada por')
    presented_date = fields.Date(
        string='Fecha presentación')
    file_number = fields.Char(
        string='Número expediente')
    license_concession = fields.Date(
        string='Fecha concesión')
    bonification = fields.Selection([
            ('no', 'No'),
            ('yes', 'Yes'),
            ('yes-presented', 'Yes, presented')
        ],
        string='Bonification (ICIO)')
    icio_bonification_requested_by = fields.Selection([
        ('ecooo', 'Ecooo'),
        ('client', 'Client'),
        ('not-needed', 'Not needed')
        ],
        string='Requested by'
    )
    pay_taxes = fields.Selection(
        [('ecooo', 'Ecooo'), ('participant', 'Participante'), ('other', 'Otro')],
        string='Quien paga tasas')
    license_notes = fields.Text(
        string='Notas licencia')
    ovp_request = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
        ('not-needed', 'Not needed')
        ],
        string='Request OVP')
    ovp_request_date = fields.Date(
        string='OVP request date'
    )
    ovp_approval_date = fields.Date(
        string='OVP approval date'
    )
    ovp_ammount = fields.Monetary(
        string="OVP ammount"
    )
    end_of_work_notified = fields.Boolean(
        string="End of work notified"
    )
    customer_shipments = fields.Char(
        string="Customer shipment"
    )
    ibi_bonification_requested_by = fields.Selection([
            ('ecooo', 'Ecooo'),
            ('client', 'Client')
        ],
        string='Requested by'
    )
    ibi_bonification_request_date = fields.Date(
        string="Request date"
    )
    ibi_bonification=fields.Boolean(
        string='Concession'
    )
    legal_requirements_ids = fields.One2many(
        comodel_name='installation.legal.requirement',
        inverse_name='installation_id',
        string='Legal requirement'
    )

    # Needed for monetary fields
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related="company_id.currency_id", string="Currency", readonly=True)

    # Subvención
    subvention_selection = fields.Selection(
        [('yes', 'Si'), ('no', 'No')],
        string='Solicita subvención')
    subvention_type = fields.Char(
        string='Tipo subvención')
    subvention_request_date = fields.Date(
        string='Fecha solicitud')
    file_number_subvention = fields.Char(
        string='Número expediente')
    subvention_requirement_date = fields.Date(
        string='Fecha requerimientos')
    subvention_response_date = fields.Date(
        string='Respuesta requerimiento s')
    subvention_concession = fields.Date(
        string='Fecha concesión subv')
    subvention_funds_approval_date = fields.Date(
        string='Funds approval date'
    )
    subvention_justification_deadline = fields.Date(
        string='Justification deadline'
    )
    subvention_justification_submission_date=fields.Date(
        string="Justification submission date"
    )
    subvention_notes = fields.Text(
        string='Notas subvención')

    # Tramitación
    cau = fields.Char(
        string='CAU'
    )
    file_number_processing = fields.Char(
        string='File number processing'
    )
    aditional_files=fields.Char(
        string='Old, closed or additional files'
    )
    management_contact=fields.Many2one(
        comodel_name='res.partner',
        string='Management Contact'
    )

    management_contact_tag=fields.Many2one(
        comodel_name='res.partner.category',
        compute='_compute_management_contact_tag',
        store=False
    )

    technical_conditions=fields.Selection([
            ('yes', 'Yes'),
            ('no', 'No'),
            ('not-needed', 'No, not needed')
        ],
        string='Technical and economic conditions'
    )
    cta=fields.Selection([
            ('yes', 'Yes'),
            ('no', 'No'),
            ('not-needed', 'No, not needed')
        ],
        string="CTA and close"
    )
    approval_number=fields.Char(
        string="Nº of approval"
    )
    approval_date=fields.Date(
        string="Date of approval"
    )
    periodic_inspection=fields.Boolean(
        string="Periodic inspection"
    )
    installer_send_date=fields.Date(
        string="Installer send date"
    )
    registry_send_date=fields.Date(
        string="Registry send date"
    )
    cie_resgistry_date = fields.Date(
        string="CIE registry date"
    )
    inspection_date=fields.Date(
        string="Inspection date"
    )
    cie_registry_state=fields.Selection(
        [('awaintin_customer', 'Awaiting customer'),
        ('awaiting_installer', 'Awaiting installer'),
        ('in_process', 'In process'),
        ('completed', 'Completed')],
        string="CIE registry state"
    )
    documentation_sent=fields.Boolean(
        string="Documentation sent"
    )
    meter_verification=fields.Date(
        string="Meter verified"
    )

    transaction_notes = fields.Text(
        string='Notas tramitación')    


    #Hitos
    first_milestone_payed = fields.Boolean(
        string='First milestone payed'
    )
    personalized_studies = fields.Boolean(
        string='Personalized studies'
    )
    documentation_delivered = fields.Boolean(
        string='Documentation delivered'
    )
    draft_ready_for_submission = fields.Boolean(
        string='Draft ready for submission'
    )
    draft_sent = fields.Boolean(
        string='Draft sent'
    )
    draft_sent_date = fields.Date(
        string='Draft sent date'
    )
    contract_signed = fields.Boolean(
        string='Contract signed'
    )
    payment_method_chosen = fields.Boolean(
        string='Payment method chosen'
    )
    distribution_agreement_signed = fields.Boolean(
        string='Distribution agreement signed'
    )
    second_milestone_payed = fields.Boolean(
        string='Second milestone payed'
    )
    payment_date = fields.Date(
        string='Payment date'
    )
    representation_letter_received = fields.Boolean(
        string='Representation letter recieved'
    )
    construction_scheduled = fields.Boolean(
        string='Scheduled',
        compute='_compute_construction_scheduled'
    )
    installation_date_confirmed = fields.Boolean(
        string='Installation date confirmed'
    )
    responsible_statement_presented = fields.Boolean(
        string='Responsible statement presented',
        compute='_compute_responsible_statement_presented'
    )
    installation_date_reminder = fields.Boolean(
        string='Installation date reminder'
    )
    end_of_work_completed = fields.Boolean(
        string='End of work completed'
    )
    client_documentation_sent=fields.Boolean(
        string='Client documentation sent'
    )
    payment_pending=fields.Boolean(
        string='Payment pending'
    )
    notification_one_month_after_execution=fields.Boolean(
        string='Notifaction one month after execution'
    )
    notification_one_year_after_execution=fields.Boolean(
        string='Notifaction one year after execution'
    )
    notification_warranty_expired=fields.Boolean(
        string='Notifaction warranty expired'
    )



    sale_order_ids = fields.One2many(
        comodel_name="sale.order", inverse_name="installation_id", string="Pedidos de venta"
    )
    purchase_order_ids = fields.One2many(
        comodel_name="purchase.order", inverse_name="installation_id", string="Pedidos de compra"
    )

    invoice_ids = fields.One2many(
        comodel_name="account.move", inverse_name="installation_id", string="Facturas"
    )

    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account", string="Analytic account"
    )

    sale_orders_count = fields.Integer(string="Pedidos de venta", compute="_compute_sale_orders")
    purchase_orders_count = fields.Integer(string="Pedidos de compra", compute="_compute_purchase_orders")
    invoices_count = fields.Integer(string="Facturas", compute="_compute_invoices")

    role_ids = fields.One2many(
        comodel_name='installation.role.line',
        inverse_name='installation_id',
        string='Roles')

    def _compute_sale_orders(self):
        for record in self:
            record.sale_orders_count = len(record.sale_order_ids)

    def _compute_purchase_orders(self):
        for record in self:
            record.purchase_orders_count = len(record.purchase_order_ids)

    def _compute_invoices(self):
        for record in self:
            record.invoices_count = len(record.invoice_ids)

    @api.depends('construction_start_date')
    def _compute_construction_scheduled(self):
        for record in self:
            record.construction_scheduled = True if record.construction_start_date else False

    @api.depends('construction_start_date')
    def _compute_construction_week(self):
        for record in self:
            record.week_construction = record.construction_start_date.isocalendar()[1] if record.construction_start_date else False

    @api.onchange('partner_id2')
    def _onchange_partner_id2(self):
        if self.partner_id2:
            self.partner_id2_name = self.partner_id2.firstname or self.partner_id2.name
            self.partner_id2_surname = self.partner_id2.lastname
            self.partner_id2_vat = self.partner_id2.vat
            self.supply_street = self.partner_id2.street
            self.supply_zip = self.partner_id2.zip
    
    @api.depends('presented_date')
    def _compute_responsible_statement_presented(self):
        for record in self:
            record.responsible_statement_presented = True if record.presented_date else False

    @api.depends('inverter_ids')
    def _compute_rated_power(self):
        self.rated_power_execution = sum(inverter.power for inverter in self.inverter_ids)

    @api.depends('module_ids')
    def _compute_peak_power(self):
        self.peak_power_execution = sum(module.power*module.number_of_modules for module in self.module_ids)/1000

    def _compute_management_contact_tag(self):
        self.management_contact_tag = int(self.env['ir.config_parameter'].sudo().get_param('file_manager_tag'))
    
    def _compute_supplier_tag(self):
        self.supplier_tag = int(self.env['ir.config_parameter'].sudo().get_param('supplier_tag'))
    
    def _compute_installer_tag(self):
        self.installer_tag = int(self.env['ir.config_parameter'].sudo().get_param('installer_tag'))
    
    def write(self, vals):
        res = super().write(vals)
        relevant_vals = {
            'construction_start_date',
            'construction_end_date',
            'stake_out_date',
        }
        set_vals = set(vals)
        has_relevant_vals = relevant_vals.intersection(set_vals)
        if has_relevant_vals:
            self._create_or_update_installation_event(self)
        return res

    def action_view_sale_orders(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Pedidos de venta",
            "view_mode": "tree,form",
            "res_model": "sale.order",
            "domain": [("id", "in", self.sale_order_ids.ids)],
            "context": "{'create': False}",
        }

    def action_view_purchase_orders(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Pedidos de compra",
            "view_mode": "tree,form",
            "res_model": "purchase.order",
            "domain": [("id", "in", self.purchase_order_ids.ids)],
            "context": "{'create': False}",
        }

    def action_view_invoices(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Facturas",
            "view_mode": "tree,form",
            "res_model": "account.move",
            "domain": [("id", "in", self.invoice_ids.ids)],
            "context": "{'create': False}",
        }

    def action_view_customer(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Customer",
            "view_mode": "form",
            "res_model": "res.partner",
            "res_id": self.partner_id.id
        }
    
    def action_view_analytic_account(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Analytic account",
            "view_mode": "tree",
            "res_model": "account.analytic.line",
            "domain": [("account_id", "=", self.analytic_account_id.id)],
            "context": {'search_default_group_date': 1, 'default_account_id': self.analytic_account_id.id},
            "view_id": self.env.ref('analytic.view_account_analytic_line_tree').id
        }

    def _create_or_update_installation_event(self, installation):
        events = self.env['installation.event'].search([
            ('installation_id', '=', installation.id)])
        if events:
            construction_event = next(iter([event for event in events if event.type=='obra']), None)
            stake_out_event = next(iter([event for event in events if event.type=='replanteo']), None)
        else:
            construction_event = None
            stake_out_event = None
        if installation.construction_start_date or installation.construction_end_date:
            if construction_event and (fields.Date.to_date(construction_event.start_date) != installation.construction_start_date or fields.Date.to_date(construction_event.end_date) != installation.construction_end_date):
                construction_event.write({
                    'start_date': fields.Datetime.to_datetime(installation.construction_start_date) if installation.construction_start_date else fields.Datetime.to_datetime(installation.construction_end_date), 
                    'end_date': fields.Datetime.to_datetime(installation.construction_end_date) if installation.construction_end_date else fields.Datetime.to_datetime(installation.construction_start_date)
                })
            elif not construction_event:
                vals = {'name': f'{installation.name} - Obra',
                        'installation_id': installation.id,
                        }
                vals.update(type='obra', start_date=installation.construction_start_date or installation.construction_end_date, end_date=installation.construction_end_date or installation.construction_start_date)
                self.env['installation.event'].create(vals)
        elif construction_event:
                construction_event.unlink()

        if installation.stake_out_date:
            if stake_out_event and (stake_out_event.start_date != installation.stake_out_date or stake_out_event.end_date != installation.stake_out_date):
                stake_out_event.write({
                    'start_date': installation.stake_out_date,
                    'end_date': fields.Datetime.add(installation.stake_out_date, hours=1)
                })
            elif not stake_out_event:
                vals = {'name': f'{installation.name} - Replanteo',
                        'installation_id': installation.id,
                        }
                vals.update(start_date=installation.stake_out_date, end_date=installation.stake_out_date, type='replanteo')
                self.env['installation.event'].create(vals)
        elif stake_out_event:
            stake_out_event.unlink()

class InstallationRoleLine(models.Model):
    _name = 'installation.role.line'

    role_id = fields.Many2one(
        comodel_name='installation.role',
        string='Rol')

    responsible_candidates_ids = fields.Many2many(related='role_id.responsible_ids')

    responsible_ids = fields.Many2many(
        comodel_name='res.users',
        string='Coordinadores')

    installation_id = fields.Many2one(
        comodel_name='selfconsumption.installation',
        string='Instalación')

class InstallationInveter(models.Model):
    _name = 'installation.inverter'
    _description = 'Inverter asociated with an installation'

    installation_id = fields.Many2one(
        string = 'Installation',
        comodel_name='selfconsumption.installation',
        index=True,
        ondelete='cascade'
    )

    inverter_id = fields.Many2one(
        string = 'Model',
        comodel_name='photovoltaic.inverter',
        ondelete='cascade'
    )

    power = fields.Float(
        related='inverter_id.rated_power_ac',
        string='Power (kW)'
    )

    intensity=fields.Float(
        related='inverter_id.maximun_current_ac',
        string='Intensity'
    )

    serial_number=fields.Char(
        string='Serial number'
    )

class InstallationModule(models.Model):
    _name = 'installation.module'
    _description = 'Module asociated with an installation'

    installation_id = fields.Many2one(
        string = 'Installation',
        comodel_name='selfconsumption.installation',
        index=True,
        ondelete='cascade'
    )

    module_id = fields.Many2one(
        string='Model',
        comodel_name='photovoltaic.module',
        ondelete='cascade'
    )

    power = fields.Float(
        string='Power (W)',
        related='module_id.power'
    )

    intensisty = fields.Float(
        string='Intensity',
        related='module_id.max_current'
    )

    number_of_modules = fields.Integer(
        string='Nº of modules'
    )
    
class InstallationLegalRequirement(models.Model):
    _name = 'installation.legal.requirement'
    _description= 'Legal requirement asociated with an installation'

    installation_id = fields.Many2one(
        string = 'Installation',
        comodel_name='selfconsumption.installation',
        index=True,
        ondelete='cascade'
    )

    type = fields.Char(
        string='Type'
    )

    limit_date = fields.Date(
        string='Limit date'
    )

    response_date = fields.Date(
        string='Response date'
    )

    done = fields.Boolean(
        string='Done'
    )

    manager_id = fields.Many2one(
        string='Manager',
        comodel_name='hr.employee',
        index=True,
        ondelete='restrict'
    )

    notes = fields.Char(
        string='Notes'
    )

    installation_event_id = fields.Many2one(
        comodel_name='installation.event',
        ondelete='cascade'
    )

    def create(self, vals):
        res = super().create(vals)
        self.__create_or_update_requirement_event(res)
        return res

    def write(self, vals):
        res = super().write(vals)
        relevant_vals = {
            'limit_date',
            'done'
        }
        set_vals = set(vals)
        has_relevant_vals = relevant_vals.intersection(set_vals)
        if has_relevant_vals:
            self.__create_or_update_requirement_event(self)
        return res

    def unlink(self):
        for requierement in self:
            if requierement.installation_event_id and requierement.installation_event_id.exists():
                self.env['installation.event'].browse([requierement.installation_event_id.id]).unlink()
        super().unlink()
    
    def __create_or_update_requirement_event(self, requirement):
        if requirement.installation_event_id:
            requirement.installation_event_id.start_date=requirement.limit_date
            requirement.installation_event_id.end_date=requirement.limit_date
            requirement.installation_event_id.name = f'{requirement.installation_id.name} - Requerimiento - {requirement.type}{" (Hecho)" if requirement.done else ""}'
        else:
            event = self.env['installation.event'].create({
                'installation_id': requirement.installation_id.id,
                'name': f'{requirement.installation_id.name} - Requerimiento - {requirement.type}{" (Hecho)" if requirement.done else ""}',
                'start_date': requirement.limit_date,
                'end_date': requirement.limit_date,
                'type': 'requerimiento'
            })
            requirement.installation_event_id = event.id