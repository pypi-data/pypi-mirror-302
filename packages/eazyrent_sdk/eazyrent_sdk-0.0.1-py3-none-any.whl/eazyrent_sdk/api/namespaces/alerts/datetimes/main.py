from datetime import date, datetime, timedelta

# from dateutil.relativedelta import relativedelta


class DateTimes:
    def validate_expiry_date(
        self,
        expiry_date: date | datetime,
        delta: timedelta | None = None,
    ) -> bool:
        """Check if an expiry date is in the past.

        args:
            - expiry_date: (date | datetime) the expiry date to validate
            - delta: (timedelta | relativedelta | None)
                A temporal window that will be added to the current datetime.

        returns:
            - valid (bool): True if the expiry date is valid.
        """
        now = datetime.now()
        if delta is not None:
            now += delta
        return now > expiry_date
