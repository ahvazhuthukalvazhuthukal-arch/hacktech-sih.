"""
KalaiPaalam AI - Buyer Catalog & D2C Storefront API
Public buyer-facing endpoints for craft discovery, filtering, and ordering.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import json
import uuid

from app.models.schema import Product, OrderRecord
from app.services.database import get_db
from app.api.products import _format_product_response

router = APIRouter(prefix="/api/catalog", tags=["Buyer Catalog"])

@router.get("/")
def get_buyer_catalog(
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product).filter(Product.status.in_(["PUBLISHED", "READY"]))
    if category and category != "All":
        query = query.filter(Product.category == category)
    if search:
        query = query.filter(Product.title.ilike(f"%{search}%"))

    products = query.order_by(Product.created_at.desc()).all()
    catalog = []
    for p in products:
        catalog.append(_format_product_response(p, db))
    return catalog

@router.get("/{product_id}")
def get_catalog_product_detail(product_id: str, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found in catalog")
    return _format_product_response(p, db)

@router.post("/order")
def place_mock_order(payload: Dict[str, Any], db: Session = Depends(get_db)):
    product_id = payload.get("product_id")
    quantity = int(payload.get("quantity", 1))
    buyer_name = payload.get("buyer_name", "Verified Buyer")

    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")

    if p.inventory < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    p.inventory -= quantity
    order_id = f"KP-ORD-{uuid.uuid4().hex[:6].upper()}"

    order = OrderRecord(
        id=str(uuid.uuid4()),
        external_order_id=order_id,
        marketplace="KalaiPaalam Catalog",
        product_id=p.id,
        product_title=p.title,
        quantity=quantity,
        amount=p.price * quantity,
        buyer_name=buyer_name,
        shipping_status="CONFIRMED"
    )
    db.add(order)
    db.commit()

    return {
        "success": True,
        "order_id": order_id,
        "product_id": p.id,
        "quantity": quantity,
        "total_amount": order.amount,
        "remaining_inventory": p.inventory,
        "message": "Order placed successfully. Inventory updated."
    }
