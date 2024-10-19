import os
from typing import Any

import httpx


class TaxNotices:
    def get_notice_existence(self, tax_number: str, notice_reference: str) -> Any:
        url = os.environ.get("EAZYRENT_API_TAX_NOTICE__ENDPOINT", "").format(
            tax_number=tax_number,
            notice_reference=notice_reference,
        )
        response = httpx.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
