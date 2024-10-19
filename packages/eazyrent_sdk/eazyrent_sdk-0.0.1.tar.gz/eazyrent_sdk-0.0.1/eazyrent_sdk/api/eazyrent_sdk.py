from .namespaces.alerts import AlertSDK


class EazyrentSDK:
    def __init__(self):
        self.alerts = AlertSDK()
