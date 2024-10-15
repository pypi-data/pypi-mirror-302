from policyengine_us.model_api import *


class de_income_tax_before_non_refundable_credits_joint(Variable):
    value_type = float
    entity = Person
    label = "Delaware personal income tax before non-refundable credits when married filing jointly"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.DE

    def formula(person, period, parameters):
        taxable_income = person("de_taxable_income_joint", period)
        p = parameters(period).gov.states.de.tax.income
        return p.rate.calc(taxable_income)
