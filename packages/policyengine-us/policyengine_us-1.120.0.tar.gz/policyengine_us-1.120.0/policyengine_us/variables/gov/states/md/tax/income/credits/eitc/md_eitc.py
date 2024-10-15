from policyengine_us.model_api import *


class md_eitc(Variable):
    value_type = float
    entity = TaxUnit
    label = "MD total EITC"
    unit = USD
    documentation = "Refundable and non-refundable Maryland EITC"
    definition_period = YEAR
    reference = "https://casetext.com/statute/code-of-maryland/article-tax-general/title-10-income-tax/subtitle-7-income-tax-credits/section-10-704-effective-until-6302023-for-earned-income"
    defined_for = StateCode.MD

    adds = ["md_non_refundable_eitc", "md_refundable_eitc"]
