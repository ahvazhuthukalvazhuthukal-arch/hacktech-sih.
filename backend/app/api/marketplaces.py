"""
KalaiPaalam AI - Marketplace Channels & Connections Endpoints
Implements "Connect Your Stores", Capability Negotiation, and Protocol Payload Inspection.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import json
from datetime import datetime, timezone

from app.models.schema import MarketplaceConnection, Product
from app.services.database import get_db
from app.connectors.registry import connector_registry

router = APIRouter(prefix="/api/marketplaces", tags=["Marketplaces"])

@router.get("/")
def list_marketplaces(db: Session = Depends(get_db)):
    """
    Returns all supported sales channels with their connection state,
    negotiated capabilities, environment badges, and last synced timestamps.
    """
    db_connections = db.query(MarketplaceConnection).all()
    conn_map = {c.marketplace: c for c in db_connections}

    channels_data = []
    registered = connector_registry.list_connectors()

    for item in registered:
        m_name = item["marketplace"]
        db_conn = conn_map.get(m_name)

        status = db_conn.status if db_conn else item.get("status", "NOT_CONNECTED")
        account_name = db_conn.account_name if db_conn else item.get("account_name", "")
        last_synced = db_conn.last_synced_at.isoformat() if (db_conn and db_conn.last_synced_at) else None

        channels_data.append({
            "marketplace": m_name,
            "status": status,
            "account_name": account_name,
            "external_account_id": item.get("external_account_id"),
            "environment": item.get("environment", "DEMO"),
            "capabilities": item.get("capabilities", []),
            "last_synced_at": last_synced
        })

    return channels_data

@router.post("/connect")
def connect_marketplace(payload: Dict[str, Any], db: Session = Depends(get_db)):
    """
    Simulates OAuth / Token Authorization flow:
    Artisan authorizes KalaiPaalam -> Stores secure token reference (NEVER plaintext passwords).
    """
    marketplace = payload.get("marketplace")
    if not marketplace:
        raise HTTPException(status_code=400, detail="Marketplace name required")

    conn = db.query(MarketplaceConnection).filter_by(marketplace=marketplace).first()
    if not conn:
        conn = MarketplaceConnection(
            id=f"conn_{marketplace.lower().replace(' ', '_')}",
            artisan_id="artisan_demo_01",
            marketplace=marketplace,
            connection_type="OAUTH_TOKEN",
            status="CONNECTED",
            account_name=f"{marketplace} Connected Account",
            external_account_id=f"{marketplace[:3].upper()}-REF-{marketplace.lower()[:3]}",
            access_token_reference=f"vault://{marketplace.lower()}-token-ref",
            connected_at=datetime.now(timezone.utc),
            last_synced_at=datetime.now(timezone.utc),
            capabilities_json=json.dumps(["CREATE_LISTING", "UPDATE_PRICE", "UPDATE_INVENTORY"]),
            environment="DEMO"
        )
        db.add(conn)
    else:
        conn.status = "CONNECTED"
        conn.last_synced_at = datetime.now(timezone.utc)

    db.commit()
    return {"success": True, "marketplace": marketplace, "status": "CONNECTED", "environment": conn.environment}

@router.post("/disconnect")
def disconnect_marketplace(payload: Dict[str, Any], db: Session = Depends(get_db)):
    marketplace = payload.get("marketplace")
    conn = db.query(MarketplaceConnection).filter_by(marketplace=marketplace).first()
    if conn:
        conn.status = "DISCONNECTED"
        db.commit()
    return {"success": True, "marketplace": marketplace, "status": "DISCONNECTED"}

@router.get("/{marketplace}/payload/{product_id}")
def inspect_marketplace_payload(marketplace: str, product_id: str, db: Session = Depends(get_db)):
    """
    Returns exact channel-specific protocol payload generated from canonical product.
    Allows judges to verify Beckn ONDC, GeM feed, Amazon SP-API, and Flipkart schemas.
    """
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")

    conn = connector_registry.get_connector(marketplace)
    if not conn:
        raise HTTPException(status_code=404, detail=f"No connector for {marketplace}")

    from app.api.products import _format_product_response
    canonical_dict = _format_product_response(p, db)
    validation = conn.validate_canonical_product(canonical_dict)
    payload = conn.map_to_payload(canonical_dict)

    return {
        "marketplace": marketplace,
        "environment": conn.environment.value,
        "product_id": p.id,
        "validation": validation,
        "generated_protocol_payload": payload
    }
