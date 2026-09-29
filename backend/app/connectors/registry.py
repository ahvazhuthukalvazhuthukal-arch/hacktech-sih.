"""
KalaiPaalam AI - Central Marketplace Connector Registry
Discovers, manages, and executes multi-channel connector operations.
Implements the central vision:
ONE ARTISAN -> ONE CANONICAL PRODUCT -> MANY MARKETPLACES
"""

from typing import Dict, Any, List, Optional
from app.connectors.base import BaseMarketplaceConnector, ConnectorEnvironment, ConnectionStatus
from app.connectors.ondc.adapter import ONDCConnector
from app.connectors.gem.adapter import GeMConnector
from app.connectors.amazon.adapter import AmazonConnector
from app.connectors.flipkart.adapter import FlipkartConnector
from app.connectors.storefront.adapter import StorefrontConnector
from app.connectors.demo.adapter import DemoMarketplaceConnector

class MarketplaceConnectorRegistry:
    def __init__(self):
        self._connectors: Dict[str, BaseMarketplaceConnector] = {}
        self._register_default_connectors()

    def _register_default_connectors(self):
        # Register standard suite
        self.register("ONDC", ONDCConnector(ConnectorEnvironment.DEMO))
        self.register("GeM", GeMConnector(ConnectorEnvironment.DEMO))
        self.register("Amazon", AmazonConnector(ConnectorEnvironment.DEMO))
        self.register("Flipkart", FlipkartConnector(ConnectorEnvironment.DEMO))
        self.register("KalaiPaalam Catalog", StorefrontConnector(ConnectorEnvironment.LIVE))

    def register(self, name: str, connector: BaseMarketplaceConnector):
        key = name.lower().replace(" ", "_")
        self._connectors[key] = connector

    def get_connector(self, name: str) -> Optional[BaseMarketplaceConnector]:
        key = name.lower().replace(" ", "_")
        if key in self._connectors:
            return self._connectors[key]
        # Return fallback demo connector for unknown channels
        return DemoMarketplaceConnector(name)

    def list_connectors(self) -> List[Dict[str, Any]]:
        results = []
        for name, conn in self._connectors.items():
            results.append(conn.get_connection_status())
        return results

    def publish_to_channels(self, canonical_product: Dict[str, Any], channel_names: List[str]) -> Dict[str, Any]:
        """
        Takes one canonical product and publishes to all selected marketplace channels.
        Validates individual channel constraints and generates channel-specific payloads.
        """
        results = {}
        for ch_name in channel_names:
            conn = self.get_connector(ch_name)
            if not conn:
                results[ch_name] = {
                    "success": False,
                    "status": "UNAVAILABLE",
                    "error": f"Connector for {ch_name} is not registered."
                }
                continue

            try:
                # 1. Validate against destination schema
                val = conn.validate_canonical_product(canonical_product)
                if not val["valid"]:
                    results[ch_name] = {
                        "success": False,
                        "status": "BLOCKED",
                        "missing_fields": val["missing_fields"],
                        "error": f"Required fields missing: {', '.join(val['missing_fields'])}"
                    }
                    continue

                # 2. Execute create_listing
                res = conn.create_listing(canonical_product)
                results[ch_name] = res
            except Exception as e:
                results[ch_name] = {
                    "success": False,
                    "status": "FAILED",
                    "error": str(e)
                }

        return results

    def sync_price_across_channels(self, channel_listings: List[Dict[str, Any]], new_price: float) -> Dict[str, Any]:
        """
        Propagates updated price from single KalaiPaalam change to all connected channels.
        """
        sync_results = {}
        for item in channel_listings:
            ch_name = item.get("marketplace")
            ext_id = item.get("external_listing_id")
            conn = self.get_connector(ch_name)
            if conn:
                res = conn.update_price(ext_id, new_price)
                sync_results[ch_name] = res
            else:
                sync_results[ch_name] = {"success": False, "status": "UNKNOWN_CONNECTOR"}
        return sync_results

    def sync_inventory_across_channels(self, channel_listings: List[Dict[str, Any]], new_stock: int) -> Dict[str, Any]:
        """
        Propagates stock count adjustments across all active channels.
        """
        sync_results = {}
        for item in channel_listings:
            ch_name = item.get("marketplace")
            ext_id = item.get("external_listing_id")
            conn = self.get_connector(ch_name)
            if conn:
                res = conn.update_inventory(ext_id, new_stock)
                sync_results[ch_name] = res
            else:
                sync_results[ch_name] = {"success": False, "status": "UNKNOWN_CONNECTOR"}
        return sync_results

# Global registry instance
connector_registry = MarketplaceConnectorRegistry()
