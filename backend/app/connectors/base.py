"""
KalaiPaalam AI - Base Marketplace Connector & MCP Abstraction
Defines the standard contract for all external sales channel adapters.
Guarantees strict separation of concerns, capability negotiation,
and deterministic environment labeling (LIVE, SANDBOX, DEMO, UNAVAILABLE).
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from enum import Enum

class ConnectorEnvironment(str, Enum):
    LIVE = "LIVE"
    SANDBOX = "SANDBOX"
    DEMO = "DEMO"
    UNAVAILABLE = "UNAVAILABLE"

class ConnectionStatus(str, Enum):
    NOT_CONNECTED = "NOT_CONNECTED"
    CONNECTING = "CONNECTING"
    CONNECTED = "CONNECTED"
    AUTH_REQUIRED = "AUTH_REQUIRED"
    EXPIRED = "EXPIRED"
    ERROR = "ERROR"
    DISCONNECTED = "DISCONNECTED"

class ConnectorCapability(str, Enum):
    CREATE_LISTING = "CREATE_LISTING"
    UPDATE_LISTING = "UPDATE_LISTING"
    DELETE_LISTING = "DELETE_LISTING"
    UPDATE_PRICE = "UPDATE_PRICE"
    UPDATE_INVENTORY = "UPDATE_INVENTORY"
    UPLOAD_IMAGE = "UPLOAD_IMAGE"
    GET_ORDERS = "GET_ORDERS"
    GET_LISTING_STATUS = "GET_LISTING_STATUS"
    SYNC = "SYNC"

class BaseMarketplaceConnector(ABC):
    def __init__(self, name: str, environment: ConnectorEnvironment = ConnectorEnvironment.DEMO):
        self.name = name
        self.environment = environment
        self.status = ConnectionStatus.CONNECTED

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Returns list of supported operations for this channel."""
        pass

    @abstractmethod
    def get_connection_status(self) -> Dict[str, Any]:
        """Returns connection health, auth state, account details."""
        pass

    @abstractmethod
    def authenticate(self, credentials_ref: str) -> bool:
        """Validates credentials reference (OAuth token / API key in secure vault)."""
        pass

    @abstractmethod
    def validate_canonical_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates canonical product against channel-specific mandatory schema.
        Returns: {"valid": bool, "missing_fields": List[str], "warnings": List[str]}
        """
        pass

    @abstractmethod
    def map_to_payload(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Transforms canonical product into marketplace-specific protocol payload."""
        pass

    @abstractmethod
    def create_listing(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Creates new product listing on this marketplace."""
        pass

    @abstractmethod
    def update_listing(self, external_listing_id: str, product: Dict[str, Any]) -> Dict[str, Any]:
        """Updates listing details."""
        pass

    @abstractmethod
    def update_price(self, external_listing_id: str, new_price: float) -> Dict[str, Any]:
        """Updates channel price."""
        pass

    @abstractmethod
    def update_inventory(self, external_listing_id: str, new_stock: int) -> Dict[str, Any]:
        """Updates channel stock count."""
        pass

    @abstractmethod
    def get_orders(self) -> List[Dict[str, Any]]:
        """Fetches active orders if supported by capability."""
        pass
