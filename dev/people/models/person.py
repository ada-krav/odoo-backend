from datetime import timedelta

from odoo import api, fields, models


class Person(models.Model):
    _name = "people.person"
    _description = "Person Record"

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    full_name = fields.Char(string="Full Name", compute="_concat_full_name", store=True)
    birthday = fields.Date()
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    sex = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("non-binary", "Non-Binary")],
        string="Sex"
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company.id,
    )

    @api.depends("first_name", "last_name")
    def _concat_full_name(self):
        for person in self:
            person.full_name = f"{person.first_name} {person.last_name}"

    @api.depends("birthday")
    def _compute_age(self):
        today = fields.Date.today()
        for person in self:
            if person.birthday:
                person.age = (today - person.birthday) // timedelta(days=365)
            else:
                person.age = 0
