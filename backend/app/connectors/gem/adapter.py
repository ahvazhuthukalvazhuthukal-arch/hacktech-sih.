"""
KalaiPaalam AI - GeM (Government e-Marketplace) Adapter
Integrates artisan products into the Government Procurement Feed (Womaniya / Saras / Karigar schemes).
Converts canonical products into GeM tender & direct-procurement catalogs.
"""

from typing import Dict, Any, List
import uuid
from datetime import datetime, timezone
from app.connectors.base import BaseMarketplaceConnector, ConnectorEnvironment, ConnectionStatus, ConnectorCapability

class GeMConnector(BaseMarketplaceConnector):
    def __init__(self, environment: ConnectorEnvironment = ConnectorEnvironment.DEMO):
        super().__init__("GeM", environment)
        self.seller_id = "GEM-ARTISAN-TN-441"
        self.org_type = "Self Help Group / Artisan Collective"

    def get_capabilities(self) -> List[str]:
        return [
            ConnectorCapability.CREATE_LISTING.value,
            ConnectorCapability.UPDATE_INVENTORY.value,
            ConnectorCapability.GET_LISTING_STATUS.value,
            ConnectorCapability.SYNC.value
        ]

    def get_connection_status(self) -> Dict[str, Any]:
        return {
            "marketplace": "GeM",
            "status": self.status.value,
            "environment": self.environment.value,
            "account_name": "Government e-Marketplace (GeM Karigar)",
            "external_account_id": self.seller_id,
            "org_type": self.org_type,
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
        if not product.get("country_of_origin"):
            missing.append("country_of_origin")

        return {
            "valid": len(missing) == 0,
            "missing_fields": missing,
            "warnings": warnings
        }

    def map_to_payload(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Maps canonical product into GeM Product Specification Catalog Schema."""
        item_id = product.get("product_id", f"KP-{uuid.uuid4().hex[:6]}")
        price_val = float(product.get("price", 0.0))

        return {
            "gem_product_id": f"GEM-CAT-2026-{item_id}",
            "seller_details": {
                "seller_id": self.seller_id,
                "category": "Handicraft & Handloom SHG",
                "registered_cluster": product.get("cluster_name", "Kanchipuram Heritage Guild"),
                "state": "Tamil Nadu"
            },
            "product_details": {
                "catalog_title": product.get("title", ""),
                "hindi_catalog_title": product.get("hindi_title", ""),
                "category_name": product.get("category", "Handloom"),
                "hsn_code": product.get("hsn_code", "5208"),
                "make_in_india_compliance": {
                    "is_compliant": True,
                    "local_content_percentage": 100,
                    "country_of_origin": product.get("country_of_origin", "India")
                },
                "specifications": {
                    "craft_process": product.get("craft_type", "Handloom"),
                    "raw_materials": product.get("material", ["Cotton"]),
                    "colours": product.get("colors", ["Blue"]),
                    "weight_in_grams": product.get("weight_grams", 500)
                },
                "pricing": {
                    "offered_unit_price_inr": price_val,
                    "gst_inclusive": True,
                    "minimum_order_quantity": 1
                },
                "inventory_available": int(product.get("inventory", 1)),
                "product_image_url": product.get("processed_image_url") or product.get("original_image_url", ""),
                "description": product.get("description", "")
            },
            "feed_timestamp": datetime.now(timezone.utc).isoformat()
        }

    def create_listing(self, product: Dict[str, Any]) -> Dict[str, Any]:
        validation = self.validate_canonical_product(product)
        if not validation["valid"]:
            return {
                "success": False,
                "error": f"GeM Validation failed: Missing {', '.join(validation['missing_fields'])}",
                "status": "BLOCKED"
            }

        payload = self.map_to_payload(product)
        ext_id = f"GEM-CAT-2026-{product.get('product_id', 'KP-001')}"
        return {
            "success": True,
            "marketplace": "GeM",
            "environment": self.environment.value,
            "external_listing_id": ext_id,
            "status": "PUBLISHED",
            "listing_url": f"https://gem.gov.in/products/{ext_id}",
            "payload": payload,
            "message": "GeM Buyer-Feed entry created successfully."
        }

    def update_listing(self, external_listing_id: str, product: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "success": True,
            "marketplace": "GeM",
            "external_listing_id": external_listing_id,
            "status": "SYNCED",
            "message": "GeM procurement specs updated."
        }

    def update_price(self, external_listing_id: str, new_price: float) -> Dict[str, Any]:
        # GeM typically requires price justification for procurement adjustments
        return {
            "success": True,
            "marketplace": "GeM",
            "external_listing_id": external_listing_id,
            "new_price": new_price,
            "status": "SYNCED",
            "message": f"GeM unit price updated to ₹{new_price:,.2f}"
        }

    def update_inventory(self, external_listing_id: str, new_stock: int) -> Dict[str, Any]:
        return {
            "success": True,
            "marketplace": "GeM",
            "external_listing_id": external_listing_id,
            "new_stock": new_stock,
            "status": "SYNCED",
            "message": f"GeM stock updated to {new_stock} units"
        }

    def get_orders(self) -> List[Dict[str, Any]]:
        return []
