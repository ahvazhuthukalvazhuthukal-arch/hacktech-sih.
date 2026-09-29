"""
KalaiPaalam AI - Generic Prototype / Sandbox Demonstration Connector
Simulates marketplace integration states with 100% reliability during offline or live SIH demos.
Explicitly labels environment as DEMO.
"""

from typing import Dict, Any, List
import uuid
from datetime import datetime, timezone
from app.connectors.base import BaseMarketplaceConnector, ConnectorEnvironment, ConnectionStatus, ConnectorCapability

class DemoMarketplaceConnector(BaseMarketplaceConnector):
    def __init__(self, name: str = "Demo Marketplace"):
        super().__init__(name, ConnectorEnvironment.DEMO)
        self.account_id = f"DEMO-{name.upper().replace(' ', '_')}-001"

    def get_capabilities(self) -> List[str]:
        return [
            ConnectorCapability.CREATE_LISTING.value,
            ConnectorCapability.UPDATE_PRICE.value,
            ConnectorCapability.UPDATE_INVENTORY.value,
            ConnectorCapability.GET_LISTING_STATUS.value,
            ConnectorCapability.SYNC.value
        ]

    def get_connection_status(self) -> Dict[str, Any]:
        return {
            "marketplace": self.name,
            "status": self.status.value,
            "environment": self.environment.value,
            "account_name": f"{self.name} Demo Sandbox",
            "external_account_id": self.account_id,
            "capabilities": self.get_capabilities()
        }

    def authenticate(self, credentials_ref: str) -> bool:
        self.status = ConnectionStatus.CONNECTED
        return True

    def validate_canonical_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        missing = []
        if not product.get("title"):
            missing.append("title")
        if not product.get("price"):
            missing.append("price")
        return { "valid": len(missing) == 0, "missing_fields": missing, "warnings": [] }

    def map_to_payload(self, product: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "demo_channel": self.name,
            "product_id": product.get("product_id"),
            "title": product.get("title"),
            "price": product.get("price"),
            "stock": product.get("inventory", 1),
            "simulated_at": datetime.now(timezone.utc).isoformat()
        }

    def create_listing(self, product: Dict[str, Any]) -> Dict[str, Any]:
        ext_id = f"DEMO-{self.name[:3].upper()}-{product.get('product_id', '001')}"
        return {
            "success": True,
            "marketplace": self.name,
            "environment": self.environment.value,
            "external_listing_id": ext_id,
            "status": "PUBLISHED",
            "listing_url": f"https://demo-sandbox.kalaipaalam.org/{ext_id}",
            "payload": self.map_to_payload(product),
            "message": f"Published via {self.name} Demo Connector."
        }

    def update_listing(self, external_listing_id: str, product: Dict[str, Any]) -> Dict[str, Any]:
        return { "success": True, "marketplace": self.name, "external_listing_id": external_listing_id, "status": "SYNCED" }

    def update_price(self, external_listing_id: str, new_price: float) -> Dict[str, Any]:
        return { "success": True, "marketplace": self.name, "external_listing_id": external_listing_id, "new_price": new_price, "status": "SYNCED" }

    def update_inventory(self, external_listing_id: str, new_stock: int) -> Dict[str, Any]:
        return { "success": True, "marketplace": self.name, "external_listing_id": external_listing_id, "new_stock": new_stock, "status": "SYNCED" }

    def get_orders(self) -> List[Dict[str, Any]]:
        return []
