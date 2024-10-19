"""Alert namespace."""

from eazyrent_sdk.interfaces.alerts import Alert, AlertType
from eazyrent_sdk.interfaces.types import ALERT_STATUS

from .datetimes import DateTimes
from .externals import ExternalServices
from .strings import Strings


class AlertSDK:
    """All related utils for alert hooks."""

    def __init__(self):
        self.external_services: ExternalServices = ExternalServices()
        self.strings: Strings = Strings()
        self.datetimes: DateTimes = DateTimes()

    def create_alert(
        self,
        alert_type: AlertType,
        level: ALERT_STATUS = "NEUTRAL",
        description: str | None = None,
    ) -> Alert:
        return Alert(alert_type=alert_type, status=level, comment=description)
