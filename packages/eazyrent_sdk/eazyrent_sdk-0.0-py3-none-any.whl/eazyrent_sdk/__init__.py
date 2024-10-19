from importlib.metadata import version
from .api import EazyrentSDK

__version__ = version("eazyrent_sdk")

__all__ = ["EazyrentSDK"]
