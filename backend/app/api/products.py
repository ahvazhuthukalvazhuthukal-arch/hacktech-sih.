"""
KalaiPaalam AI - Product Management Endpoints
Implements canonical product CRUD, AI processing dispatch, approval, and channel publishing.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import json
import uuid
from datetime import datetime, timezone

from app.models.schema import Product, ArtisanProfile, Listing, PriceRecommendation, MarketplaceListing, SyncJob, AuditLog
from app.services.database import get_db
from app.ai.orchestrator import ai_orchestrator
from app.connectors.registry import connector_registry
from app.services.pricing_service import pricing_service

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/")
def list_products(
    category: Optional[str] = None,
    status: Optional[str] = None,
    artisan_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    if status:
        query = query.filter(Product.status == status)
    if artisan_id:
        query = query.filter(Product.artisan_id == artisan_id)
    
    products = query.order_by(Product.created_at.desc()).all()
    results = []
    for p in products:
        results.append(_format_product_response(p, db))
    return results

@router.get("/{product_id}")
def get_product(product_id: str, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return _format_product_response(p, db)

@router.post("/draft")
def create_draft(data: Dict[str, Any], db: Session = Depends(get_db)):
    pid = data.get("product_id") or f"KP-{uuid.uuid4().hex[:6].upper()}"
    p = Product(
        id=pid,
        artisan_id=data.get("artisan_id", "artisan_demo_01"),
        title=data.get("title", "Draft Artisan Item"),
        category=data.get("category", "Textiles & Handloom"),
        price=data.get("price", 0.0),
        inventory=data.get("inventory", 1),
        status="DRAFT"
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"success": True, "product_id": p.id, "status": p.status}

@router.post("/ai_process")
async def process_with_ai(
    image: Optional[UploadFile] = File(None),
    voice: Optional[UploadFile] = File(None),
    spoken_text: Optional[str] = Form(None),
    language: str = Form("ta"),
    existing_image_url: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Core AI transformation:
    Takes craft photo + voice note -> returns canonical product with studio image, bilingual listing, and fair price.
    """
    image_bytes = await image.read() if image else None
    image_filename = image.filename if image else None
    voice_bytes = await voice.read() if voice else None

    # Run AI pipeline
    pipeline_result = ai_orchestrator.process_artisan_input(
        image_bytes=image_bytes,
        image_filename=image_filename,
        existing_image_url=existing_image_url,
        voice_bytes=voice_bytes,
        spoken_text=spoken_text,
        source_language=language
    )

    canonical = pipeline_result["canonical_product"]

    # Persist in DB
    new_product = Product(
        id=canonical["product_id"],
        artisan_id="artisan_demo_01",
        title=canonical["title"],
        hindi_title=canonical.get("hindi_title"),
        tamil_title=canonical.get("tamil_title"),
        category=canonical["category"],
        subcategory=canonical["subcategory"],
        craft_type=canonical["craft_type"],
        material=json.dumps(canonical["material"]),
        colors=json.dumps(canonical["colors"]),
        description=canonical["description"],
        hindi_description=canonical.get("hindi_description"),
        tamil_description=canonical.get("tamil_description"),
        dimensions_json=json.dumps(canonical["dimensions"]),
        weight_grams=canonical["weight_grams"],
        hsn_code=canonical["hsn_code"],
        country_of_origin=canonical["country_of_origin"],
        labour_hours=canonical["labour_hours"],
        material_cost=canonical["material_cost"],
        price=canonical["price"],
        inventory=canonical["inventory"],
        sku=canonical["sku"],
        original_image_url=canonical["original_image_url"],
        processed_image_url=canonical["processed_image_url"],
        voice_transcript=canonical["voice_transcript"],
        detected_language=canonical["detected_language"],
        craft_story=canonical["craft_story"],
        confidence_score=canonical["confidence_scores"].get("title", "HIGH"),
        provenance_json=json.dumps(canonical["provenance"]),
        status="READY"
    )
    db.add(new_product)

    # Persist Price Recommendation
    pricing_meta = pipeline_result["pricing_metadata"]
    pr = PriceRecommendation(
        id=f"pr_{uuid.uuid4().hex[:6]}",
        product_id=new_product.id,
        material_cost=pricing_meta["material_cost"],
        labour_hours=pricing_meta["labour_hours"],
        labour_rate=pricing_meta["labour_rate_per_hour"],
        overhead=pricing_meta["overhead_cost"],
        market_signal=pricing_meta["market_signal_multiplier"],
        base_cost=pricing_meta["base_cost"],
        recommended_low=pricing_meta["recommended_low"],
        recommended_mid=pricing_meta["recommended_mid"],
        recommended_high=pricing_meta["recommended_high"],
        explanation=pricing_meta["explanation"]
    )
    db.add(pr)

    # Persist Listing
    l = Listing(
        id=f"list_{uuid.uuid4().hex[:6]}",
        product_id=new_product.id,
        english_title=canonical["title"],
        english_description=canonical["description"],
        hindi_title=canonical["hindi_title"],
        hindi_description=canonical["hindi_description"],
        bullet_points_json=json.dumps(canonical["bullet_points"]),
        keywords=json.dumps(canonical["keywords"])
    )
    db.add(l)

    db.commit()
    db.refresh(new_product)

    return {
        "success": True,
        "product": _format_product_response(new_product, db),
        "ai_pipeline_stages": {
            "stage_1_image": pipeline_result["image_metadata"],
            "stage_2_speech": pipeline_result["speech_metadata"],
            "stage_3_extraction": {
                "confidence_scores": canonical["confidence_scores"],
                "provenance": canonical["provenance"]
            },
            "stage_4_pricing": pricing_meta
        }
    }

@router.put("/{product_id}")
def update_product(product_id: str, updates: Dict[str, Any], db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")

    if "title" in updates:
        p.title = updates["title"]
    if "hindi_title" in updates:
        p.hindi_title = updates["hindi_title"]
    if "description" in updates:
        p.description = updates["description"]
    if "category" in updates:
        p.category = updates["category"]
    if "price" in updates:
        p.price = float(updates["price"])
    if "inventory" in updates:
        p.inventory = int(updates["inventory"])
    if "hsn_code" in updates:
        p.hsn_code = updates["hsn_code"]
    if "weight_grams" in updates:
        p.weight_grams = float(updates["weight_grams"])

    p.status = "APPROVED"
    db.commit()
    db.refresh(p)
    return {"success": True, "product": _format_product_response(p, db)}

@router.post("/{product_id}/publish")
def publish_to_marketplaces(
    product_id: str,
    payload: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Core Multi-Marketplace Publishing Endpoint:
    Publishes one canonical product to multiple selected channels.
    """
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")

    channels = payload.get("channels", ["KalaiPaalam Catalog", "ONDC", "Amazon", "Flipkart"])
    canonical_dict = _format_product_response(p, db)

    publish_results = connector_registry.publish_to_channels(canonical_dict, channels)

    for ch_name, res in publish_results.items():
        status = res.get("status", "SUCCESS")
        ext_id = res.get("external_listing_id")
        
        # Upsert marketplace listing
        ml = db.query(MarketplaceListing).filter_by(product_id=p.id, marketplace=ch_name).first()
        if not ml:
            ml = MarketplaceListing(
                id=str(uuid.uuid4()),
                product_id=p.id,
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

        # Record Sync Job
        sj = SyncJob(
            id=str(uuid.uuid4()),
            product_id=p.id,
            marketplace=ch_name,
            operation="CREATE_LISTING",
            status="SUCCESS" if res.get("success") else "FAILED",
            external_id=ext_id,
            error_message=res.get("error")
        )
        db.add(sj)

    p.status = "PUBLISHED"
    db.commit()

    return {
        "success": True,
        "product_id": p.id,
        "results": publish_results
    }

@router.post("/{product_id}/sync_price")
def sync_price_across_stores(
    product_id: str,
    payload: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Centralized Price Synchronization:
    Updates price from e.g. ₹5,500 to ₹5,800 across ALL connected channels in one click.
    """
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")

    new_price = float(payload.get("price", p.price))
    p.price = new_price

    # Find all active marketplace listings for this product
    active_listings = db.query(MarketplaceListing).filter_by(product_id=p.id).all()
    channel_list = [
        {"marketplace": ml.marketplace, "external_listing_id": ml.external_listing_id}
        for ml in active_listings
    ]

    sync_results = connector_registry.sync_price_across_channels(channel_list, new_price)

    # Log sync jobs
    for ch_name, res in sync_results.items():
        db.add(SyncJob(
            id=str(uuid.uuid4()),
            product_id=p.id,
            marketplace=ch_name,
            operation="UPDATE_PRICE",
            status="SUCCESS" if res.get("success") else "FAILED",
            external_id=res.get("external_listing_id")
        ))

    db.commit()
    return {
        "success": True,
        "product_id": p.id,
        "new_price": new_price,
        "channel_sync_results": sync_results
    }

@router.post("/{product_id}/sync_inventory")
def sync_inventory_across_stores(
    product_id: str,
    payload: Dict[str, Any],
    db: Session = Depends(get_db)
):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")

    new_stock = int(payload.get("inventory", p.inventory))
    p.inventory = new_stock

    active_listings = db.query(MarketplaceListing).filter_by(product_id=p.id).all()
    channel_list = [
        {"marketplace": ml.marketplace, "external_listing_id": ml.external_listing_id}
        for ml in active_listings
    ]

    sync_results = connector_registry.sync_inventory_across_channels(channel_list, new_stock)
    db.commit()

    return {
        "success": True,
        "product_id": p.id,
        "new_stock": new_stock,
        "channel_sync_results": sync_results
    }

def _format_product_response(p: Product, db: Session) -> Dict[str, Any]:
    # Parse JSON fields safely
    def safe_json(val, default):
        if not val:
            return default
        try:
            return json.loads(val)
        except Exception:
            return default

    # Fetch listings
    m_listings = db.query(MarketplaceListing).filter_by(product_id=p.id).all()
    channel_map = {}
    for ml in m_listings:
        channel_map[ml.marketplace] = {
            "status": ml.status,
            "external_listing_id": ml.external_listing_id,
            "listing_url": ml.listing_url,
            "last_synced_at": ml.last_synced_at.isoformat() if ml.last_synced_at else None
        }

    # Fetch price recommendation
    pr = db.query(PriceRecommendation).filter_by(product_id=p.id).first()
    rec_range = {
        "low": pr.recommended_low if pr else p.price * 0.95,
        "mid": pr.recommended_mid if pr else p.price,
        "high": pr.recommended_high if pr else p.price * 1.05,
        "explanation": pr.explanation if pr else "Price calculated from cost baseline and market factor."
    }

    artisan_name = p.artisan.name if p.artisan else "Meenakshi Sundaram"
    cluster_name = p.artisan.cluster_name if p.artisan else "Kanchipuram Heritage Guild"

    return {
        "product_id": p.id,
        "artisan_id": p.artisan_id,
        "artisan_name": artisan_name,
        "cluster_name": cluster_name,
        "region": "Kanchipuram, Tamil Nadu",
        "title": p.title,
        "hindi_title": p.hindi_title,
        "tamil_title": p.tamil_title,
        "category": p.category,
        "subcategory": p.subcategory,
        "craft_type": p.craft_type,
        "material": safe_json(p.material, ["Cotton"]),
        "colors": safe_json(p.colors, ["Blue"]),
        "dimensions": safe_json(p.dimensions_json, {}),
        "weight_grams": p.weight_grams,
        "hsn_code": p.hsn_code,
        "country_of_origin": p.country_of_origin,
        "description": p.description,
        "hindi_description": p.hindi_description,
        "tamil_description": getattr(p, "tamil_description", None) or p.description,
        "bullet_points": safe_json(db.query(Listing).filter_by(product_id=p.id).first().bullet_points_json, []) if db.query(Listing).filter_by(product_id=p.id).first() else [],
        "labour_hours": p.labour_hours,
        "material_cost": p.material_cost,
        "price": p.price,
        "recommended_price_range": rec_range,
        "inventory": p.inventory,
        "sku": p.sku or f"SKU-{p.id}",
        "original_image_url": p.original_image_url,
        "processed_image_url": p.processed_image_url,
        "voice_transcript": p.voice_transcript,
        "detected_language": p.detected_language,
        "craft_story": p.craft_story,
        "confidence_scores": {"title": p.confidence_score, "category": "HIGH", "price": "HIGH"},
        "provenance": safe_json(p.provenance_json, {}),
        "status": p.status,
        "marketplace_channels": channel_map,
        "created_at": p.created_at.isoformat() if p.created_at else None
    }
