"""
KalaiPaalam AI - Offline-First Sync & Background Job Service
Processes queued offline drafts, manages marketplace publishing jobs,
and tracks idempotent synchronization receipts.
"""

import uuid
import json
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.schema import Product, MarketplaceListing, SyncJob, AuditLog
from app.connectors.registry import connector_registry

class SyncService:
    def process_offline_sync_batch(self, db: Session, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Receives batch of locally queued drafts & jobs from mobile device.
        Ensures idempotent insertion and dispatches to marketplace connectors.
        """
        client_timestamp = payload.get("timestamp")
        items = payload.get("items", [])
        synced_results = []

        for item in items:
            product_data = item.get("product")
            channels = item.get("channels", ["KalaiPaalam Catalog", "ONDC", "Amazon", "Flipkart"])
            local_id = item.get("local_id")
            
            # Idempotency check: see if product already exists
            product_id = product_data.get("product_id") or local_id or f"KP-{uuid.uuid4().hex[:6].upper()}"
            existing_prod = db.query(Product).filter_by(id=product_id).first()

            if not existing_prod:
                # Create product in DB
                existing_prod = Product(
                    id=product_id,
                    artisan_id=product_data.get("artisan_id", "artisan_demo_01"),
                    title=product_data.get("title", "Untitled Craft Product"),
                    hindi_title=product_data.get("hindi_title"),
                    tamil_title=product_data.get("tamil_title"),
                    category=product_data.get("category", "Textiles & Handloom"),
                    subcategory=product_data.get("subcategory", "General"),
                    craft_type=product_data.get("craft_type", "Handcrafted"),
                    material=json.dumps(product_data.get("material", ["Cotton"])),
                    colors=json.dumps(product_data.get("colors", ["Natural"])),
                    description=product_data.get("description", ""),
                    hindi_description=product_data.get("hindi_description"),
                    dimensions_json=json.dumps(product_data.get("dimensions", {})),
                    weight_grams=float(product_data.get("weight_grams", 500.0)),
                    hsn_code=product_data.get("hsn_code", "5208"),
                    country_of_origin=product_data.get("country_of_origin", "India"),
                    labour_hours=float(product_data.get("labour_hours", 16.0)),
                    material_cost=float(product_data.get("material_cost", 500.0)),
                    price=float(product_data.get("price", 2500.0)),
                    inventory=int(product_data.get("inventory", 10)),
                    original_image_url=product_data.get("original_image_url"),
                    processed_image_url=product_data.get("processed_image_url"),
                    voice_transcript=product_data.get("voice_transcript"),
                    status="APPROVED"
                )
                db.add(existing_prod)
                db.commit()
                db.refresh(existing_prod)

            # Publish to selected channels
            pub_results = connector_registry.publish_to_channels(product_data, channels)

            channel_statuses = {}
            for ch_name, res in pub_results.items():
                status = res.get("status", "SUCCESS")
                ext_id = res.get("external_listing_id")
                
                # Record in marketplace_listings table
                ml = db.query(MarketplaceListing).filter_by(product_id=existing_prod.id, marketplace=ch_name).first()
                if not ml:
                    ml = MarketplaceListing(
                        id=str(uuid.uuid4()),
                        product_id=existing_prod.id,
                        marketplace=ch_name,
                        external_listing_id=ext_id,
                        status=status,
                        listing_url=res.get("listing_url"),
                        last_synced_at=datetime.now(timezone.utc)
                    )
                    db.add(ml)
                else:
                    ml.status = status
                    ml.external_listing_id = ext_id
                    ml.last_synced_at = datetime.now(timezone.utc)

                # Record sync job
                sj = SyncJob(
                    id=str(uuid.uuid4()),
                    product_id=existing_prod.id,
                    marketplace=ch_name,
                    operation="CREATE_LISTING",
                    status="SUCCESS" if res.get("success") else "FAILED",
                    external_id=ext_id,
                    error_message=res.get("error")
                )
                db.add(sj)
                channel_statuses[ch_name] = res

            existing_prod.status = "PUBLISHED"
            db.commit()

            synced_results.append({
                "local_id": local_id,
                "server_product_id": existing_prod.id,
                "status": "SYNCED",
                "marketplace_statuses": channel_statuses
            })

        return {
            "success": True,
            "synced_count": len(synced_results),
            "results": synced_results,
            "acknowledged_at": datetime.now(timezone.utc).isoformat()
        }

sync_service = SyncService()
