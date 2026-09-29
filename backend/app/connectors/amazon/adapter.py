"""
KalaiPaalam AI - Amazon Seller Partner (SP-API / Karigar) Connector Adapter
Maps canonical product to Amazon Product Listings JSON Schema.
Supports capabilities: CREATE_LISTING, UPDATE_LISTING, UPDATE_PRICE, UPDATE_INVENTORY, ORDERS, UPLOAD_IMAGE.
"""

from typing import Dict, Any, List
import uuid
from datetime import datetime, timezone
from app.connectors.base import BaseMarketplaceConnector, ConnectorEnvironment, ConnectionStatus, ConnectorCapability

class AmazonConnector(BaseMarketplaceConnector):
    def __init__(self, environment: ConnectorEnvironment = ConnectorEnvironment.DEMO):
        super().__init__("Amazon", environment)
        self.seller_id = "AMZN-SELLER-IN-8891"
        self.marketplace_id = "A21TJRUUN4KGV"  # Amazon.in marketplace ID

    def get_capabilities(self) -> List[str]:
        return [
            ConnectorCapability.CREATE_LISTING.value,
            ConnectorCapability.UPDATE_LISTING.value,
            ConnectorCapability.UPDATE_PRICE.value,
            ConnectorCapability.UPDATE_INVENTORY.value,
            ConnectorCapability.UPLOAD_IMAGE.value,
            ConnectorCapability.GET_ORDERS.value,
            ConnectorCapability.SYNC.value
        ]

    def get_connection_status(self) -> Dict[str, Any]:
        return {
            "marketplace": "Amazon",
            "status": self.status.value,
            "environment": self.environment.value,
            "account_name": "Kanchipuram Karigar Storefront",
            "external_account_id": self.seller_id,
            "marketplace_id": self.marketplace_id,
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
        if not product.get("weight_grams"):
            missing.append("weight_grams")
        if not product.get("hsn_code"):
            missing.append("hsn_code")
        if not product.get("bullet_points") and not product.get("description"):
            warnings.append("Bullet points improve Amazon search ranking.")

        return {
            "valid": len(missing) == 0,
            "missing_fields": missing,
            "warnings": warnings
        }

    def map_to_payload(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Maps canonical product into Amazon SP-API Listings Items schema."""
        sku = product.get("sku") or f"KP-AMZ-{uuid.uuid4().hex[:6]}"
        price_val = float(product.get("price", 0.0))
        weight_kg = float(product.get("weight_grams", 500.0)) / 1000.0
        dims = product.get("dimensions", {})

        return {
            "sku": sku,
            "marketplace_id": self.marketplace_id,
            "productType": "ETHNIC_WEAR" if "Textiles" in product.get("category", "") else "HOME_DECOR",
            "requirements": "LISTING",
            "attributes": {
                "item_name": [{ "value": product.get("title", ""), "language_tag": "en_IN" }],
                "brand": [{ "value": product.get("artisan_name", "KalaiPaalam Heritage Artisans"), "language_tag": "en_IN" }],
                "bullet_point": [
                    { "value": bp, "language_tag": "en_IN" } for bp in (product.get("bullet_points") or [product.get("description", "")[:100]])
                ],
                "description": [{ "value": product.get("description", ""), "language_tag": "en_IN" }],
                "purchasable_offer": [
                    {
                        "currency": "INR",
                        "our_price": [{ "schedule": [{ "value_with_tax": price_val }] }]
                    }
                ],
                "fulfillment_availability": [
                    { "fulfillment_channel_code": "DEFAULT", "quantity": int(product.get("inventory", 1)) }
                ],
                "item_package_weight": [{ "unit": "kilograms", "value": weight_kg }],
                "item_package_dimensions": [{
                    "length": { "unit": "centimeters", "value": dims.get("length_cm", 30) },
                    "width": { "unit": "centimeters", "value": dims.get("width_cm", 20) },
                    "height": { "unit": "centimeters", "value": dims.get("height_cm", 5) }
                }],
                "country_of_origin": [{ "value": "IN" }],
                "hsn_code": [{ "value": product.get("hsn_code", "5208") }],
                "main_product_image_locator": [{
                    "media_location": product.get("processed_image_url") or product.get("original_image_url", "")
                }]
            }
        }

    def create_listing(self, product: Dict[str, Any]) -> Dict[str, Any]:
        validation = self.validate_canonical_product(product)
        if not validation["valid"]:
            return {
                "success": False,
                "error": f"Amazon validation blocked: Missing {', '.join(validation['missing_fields'])}",
                "status": "BLOCKED"
            }

        payload = self.map_to_payload(product)
        ext_id = f"DEMO-AMZ-{product.get('product_id', 'KP001')}"
        return {
            "success": True,
            "marketplace": "Amazon",
            "environment": self.environment.value,
            "external_listing_id": ext_id,
            "status": "PUBLISHED",
            "listing_url": f"https://amazon.in/dp/{ext_id}",
            "payload": payload,
            "message": "Amazon Karigar listing generated and published."
        }

    def update_listing(self, external_listing_id: str, product: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "success": True,
            "marketplace": "Amazon",
            "external_listing_id": external_listing_id,
            "status": "SYNCED",
            "message": "Amazon attributes updated."
        }

    def update_price(self, external_listing_id: str, new_price: float) -> Dict[str, Any]:
        return {
            "success": True,
            "marketplace": "Amazon",
            "external_listing_id": external_listing_id,
            "new_price": new_price,
            "status": "SYNCED",
            "message": f"Amazon SP-API price updated to ₹{new_price:,.2f}"
        }

    def update_inventory(self, external_listing_id: str, new_stock: int) -> Dict[str, Any]:
        return {
            "success": True,
            "marketplace": "Amazon",
            "external_listing_id": external_listing_id,
            "new_stock": new_stock,
            "status": "SYNCED",
            "message": f"Amazon inventory updated to {new_stock} units"
        }

    def get_orders(self) -> List[Dict[str, Any]]:
        return [
            {
                "order_id": "402-9812441-1002341",
                "marketplace": "Amazon",
                "item": "Handwoven Cotton Floral Border Saree",
                "quantity": 1,
                "price": 5500.0,
                "buyer": "Priya Sharma (Chennai)",
                "status": "DISPATCH_PENDING"
            }
        ]
