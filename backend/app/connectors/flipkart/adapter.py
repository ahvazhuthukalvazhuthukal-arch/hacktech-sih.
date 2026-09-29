"""
KalaiPaalam AI - Flipkart Samarth Marketplace Adapter
Maps canonical product to Flipkart Marketplace Seller Listings schema.
"""

from typing import Dict, Any, List
import uuid
from datetime import datetime, timezone
from app.connectors.base import BaseMarketplaceConnector, ConnectorEnvironment, ConnectionStatus, ConnectorCapability

class FlipkartConnector(BaseMarketplaceConnector):
    def __init__(self, environment: ConnectorEnvironment = ConnectorEnvironment.DEMO):
        super().__init__("Flipkart", environment)
        self.seller_id = "FK-SMT-7720"

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
            "marketplace": "Flipkart",
            "status": self.status.value,
            "environment": self.environment.value,
            "account_name": "Flipkart Samarth Artisan Hub TN",
            "external_account_id": self.seller_id,
            "capabilities": self.get_capabilities()
        }

    def authenticate(self, credentials_ref: str) -> bool:
        self.status = ConnectionStatus.CONNECTED
        return True

    def validate_canonical_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        missing = []
        warnings = []
        if not product.get("title"):
            missing.append("title")
        if not product.get("price") or product.get("price") <= 0:
            missing.append("price")
        if not product.get("hsn_code"):
            missing.append("hsn_code")

        return {
            "valid": len(missing) == 0,
            "missing_fields": missing,
            "warnings": warnings
        }

    def map_to_payload(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Maps canonical product into Flipkart Listings Item schema."""
        sku = product.get("sku") or f"FK-KP-{uuid.uuid4().hex[:6]}"
        price_val = float(product.get("price", 0.0))

        return {
            "product_id": sku,
            "listing_details": {
                "mrp": price_val * 1.15,
                "selling_price": price_val,
                "listing_status": "ACTIVE",
                "hsn": product.get("hsn_code", "5208"),
                "shipping_profile": {
                    "procurement_type": "EXPRESS",
                    "shipping_provider": "FLIPKART",
                    "package_weight_kg": float(product.get("weight_grams", 500.0)) / 1000.0
                }
            },
            "inventory_details": {
                "locations": [{ "location_id": "LOC-KANCHI-01", "stock_count": int(product.get("inventory", 1)) }]
            },
            "attributes": {
                "title": product.get("title", ""),
                "description": product.get("description", ""),
                "craft_type": product.get("craft_type", "Handloom"),
                "material": product.get("material", ["Cotton"]),
                "primary_image": product.get("processed_image_url") or product.get("original_image_url", ""),
                "country_of_origin": product.get("country_of_origin", "India")
            }
        }

    def create_listing(self, product: Dict[str, Any]) -> Dict[str, Any]:
        validation = self.validate_canonical_product(product)
        if not validation["valid"]:
            return {
                "success": False,
                "error": f"Flipkart validation failed: Missing {', '.join(validation['missing_fields'])}",
                "status": "BLOCKED"
            }

        payload = self.map_to_payload(product)
        ext_id = f"DEMO-FK-{product.get('product_id', 'KP001')}"
        return {
            "success": True,
            "marketplace": "Flipkart",
            "environment": self.environment.value,
            "external_listing_id": ext_id,
            "status": "PUBLISHED",
            "listing_url": f"https://flipkart.com/p/{ext_id}",
            "payload": payload,
            "message": "Flipkart Samarth catalog listing published."
        }

    def update_listing(self, external_listing_id: str, product: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "success": True,
            "marketplace": "Flipkart",
            "external_listing_id": external_listing_id,
            "status": "SYNCED",
            "message": "Flipkart attributes updated."
        }

    def update_price(self, external_listing_id: str, new_price: float) -> Dict[str, Any]:
        return {
            "success": True,
            "marketplace": "Flipkart",
            "external_listing_id": external_listing_id,
            "new_price": new_price,
            "status": "SYNCED",
            "message": f"Flipkart price synchronized to ₹{new_price:,.2f}"
        }

    def update_inventory(self, external_listing_id: str, new_stock: int) -> Dict[str, Any]:
        return {
            "success": True,
            "marketplace": "Flipkart",
            "external_listing_id": external_listing_id,
            "new_stock": new_stock,
            "status": "SYNCED",
            "message": f"Flipkart stock synchronized to {new_stock} units"
        }

    def get_orders(self) -> List[Dict[str, Any]]:
        return []
