"""
KalaiPaalam AI - ONDC (Open Network for Digital Commerce) Protocol Adapter
Converts canonical product model into Beckn Protocol v1.2.0 catalog schema (BAP / BPP).
"""

from typing import Dict, Any, List
import uuid
from datetime import datetime, timezone
from app.connectors.base import BaseMarketplaceConnector, ConnectorEnvironment, ConnectionStatus, ConnectorCapability

class ONDCConnector(BaseMarketplaceConnector):
    def __init__(self, environment: ConnectorEnvironment = ConnectorEnvironment.DEMO):
        super().__init__("ONDC", environment)
        self.account_id = "ONDC-NODE-TN-982"
        self.provider_id = "BPP-KANCHI-WEAVERS-01"

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
            "marketplace": "ONDC",
            "status": self.status.value,
            "environment": self.environment.value,
            "account_name": "Kanchi Craft BPP Node (Beckn Protocol)",
            "external_account_id": self.account_id,
            "provider_id": self.provider_id,
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
        if product.get("inventory") is None:
            missing.append("inventory")
        if not product.get("hsn_code"):
            missing.append("hsn_code")

        return {
            "valid": len(missing) == 0,
            "missing_fields": missing,
            "warnings": warnings
        }

    def map_to_payload(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Maps canonical product to standard Beckn Protocol BPP Item schema."""
        item_id = product.get("product_id", f"KP-{uuid.uuid4().hex[:6]}")
        price_val = float(product.get("price", 0.0))
        inventory_val = int(product.get("inventory", 1))

        return {
            "context": {
                "domain": "nic2004:52110",
                "country": "IND",
                "city": "std:044",
                "action": "on_search",
                "core_version": "1.2.0",
                "bpp_id": self.account_id,
                "bpp_uri": "https://ondc.kalaipaalam.org/bpp",
                "timestamp": datetime.now(timezone.utc).isoformat()
            },
            "message": {
                "catalog": {
                    "bpp/descriptor": {
                        "name": "KalaiPaalam Artisan Collective",
                        "symbol": "/static/images/kalaipaalam_logo.png",
                        "short_desc": "Verified Direct-from-Artisan Crafts"
                    },
                    "bpp/providers": [
                        {
                            "id": self.provider_id,
                            "descriptor": {
                                "name": product.get("artisan_name", "Meenakshi Sundaram"),
                                "short_desc": product.get("cluster_name", "Kanchipuram Heritage Guild")
                            },
                            "items": [
                                {
                                    "id": f"ONDC-{item_id}",
                                    "descriptor": {
                                        "name": product.get("title", ""),
                                        "code": product.get("sku", f"SKU-{item_id}"),
                                        "symbol": product.get("processed_image_url") or product.get("original_image_url", ""),
                                        "short_desc": product.get("description", "")[:120],
                                        "long_desc": product.get("description", ""),
                                        "images": [product.get("processed_image_url") or product.get("original_image_url", "")]
                                    },
                                    "price": {
                                        "currency": "INR",
                                        "value": f"{price_val:.2f}",
                                        "maximum_value": f"{price_val * 1.1:.2f}"
                                    },
                                    "category_id": product.get("category", "Handloom"),
                                    "fulfillment_id": "F1",
                                    "location_id": "L1",
                                    "quantity": {
                                        "available": { "count": inventory_val },
                                        "maximum": { "count": min(inventory_val, 5) }
                                    },
                                    "tags": {
                                        "hsn_code": product.get("hsn_code", "5208"),
                                        "country_of_origin": product.get("country_of_origin", "IND"),
                                        "artisan_craft": product.get("craft_type", "Handloom"),
                                        "material": ", ".join(product.get("material", [])) if isinstance(product.get("material"), list) else str(product.get("material", "")),
                                        "zero_middleman": "true"
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        }

    def create_listing(self, product: Dict[str, Any]) -> Dict[str, Any]:
        validation = self.validate_canonical_product(product)
        if not validation["valid"]:
            return {
                "success": False,
                "error": f"Validation failed: Missing {', '.join(validation['missing_fields'])}",
                "status": "BLOCKED"
            }

        payload = self.map_to_payload(product)
        ext_id = f"ONDC-{product.get('product_id', 'KP-001')}-ITEM"
        return {
            "success": True,
            "marketplace": "ONDC",
            "environment": self.environment.value,
            "external_listing_id": ext_id,
            "status": "PUBLISHED",
            "listing_url": f"https://ondc.org/catalog/{ext_id}",
            "payload": payload,
            "message": "ONDC Beckn catalog entry generated and published."
        }

    def update_listing(self, external_listing_id: str, product: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "success": True,
            "marketplace": "ONDC",
            "external_listing_id": external_listing_id,
            "status": "SYNCED",
            "message": "ONDC listing updated successfully."
        }

    def update_price(self, external_listing_id: str, new_price: float) -> Dict[str, Any]:
        return {
            "success": True,
            "marketplace": "ONDC",
            "external_listing_id": external_listing_id,
            "new_price": new_price,
            "status": "SYNCED",
            "message": f"ONDC price synchronized to ₹{new_price:,.2f}"
        }

    def update_inventory(self, external_listing_id: str, new_stock: int) -> Dict[str, Any]:
        return {
            "success": True,
            "marketplace": "ONDC",
            "external_listing_id": external_listing_id,
            "new_stock": new_stock,
            "status": "SYNCED",
            "message": f"ONDC stock synchronized to {new_stock} units"
        }

    def get_orders(self) -> List[Dict[str, Any]]:
        return []
