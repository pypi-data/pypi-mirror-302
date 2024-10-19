from .companies import Companies
from .tax_notices import TaxNotices


class ExternalServices:
    def __init__(self):
        self.companies: Companies = Companies()
        self.tax_notices: TaxNotices = TaxNotices()
