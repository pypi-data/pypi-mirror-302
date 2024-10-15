import inspect
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, List, Optional, Tuple, Type, Union

from requests.auth import AuthBase

from bizon.source.models import SourceIteration

from .config import SourceConfig
from .session import Session


class AbstractSource(ABC):

    def __init__(self, config: SourceConfig):
        self.config = config
        self.session = self.get_session()

        # Set authentication in the session
        auth = self.get_authenticator()

        if auth:
            self.session.auth = auth

    def __del__(self):
        self.session.close()

    @staticmethod
    @abstractmethod
    def streams() -> List[str]:
        """Return all the streams that the source supports"""
        pass

    @staticmethod
    @abstractmethod
    def get_config_class() -> Type[SourceConfig]:
        """Return the config class for the source"""
        pass

    @abstractmethod
    def get_authenticator(self) -> Union[AuthBase, None]:
        """Return an authenticator for the source, it will be set in the session
        If no authenticator is needed, return None
        """
        pass

    @abstractmethod
    def check_connection(self) -> Tuple[bool, Optional[Any]]:
        pass

    @abstractmethod
    def get(self, pagination: dict = None) -> SourceIteration:
        """Perform next API call to retrieve data and return next pagination.

        If pagination is None, it should return the first page of data.
        Otherwise, it should return the next page of data.

        - pagination dict
        - records List[dict]
        """
        pass

    @abstractmethod
    def get_total_records_count(self) -> Optional[int]:
        """Return the total count of records available in the source"""
        pass

    def get_records_updated_after(self, after: datetime) -> SourceIteration:
        """Return the records updated after the given datetime"""
        pass

    def get_session(self) -> Session:
        """Return a new session"""
        return Session()
