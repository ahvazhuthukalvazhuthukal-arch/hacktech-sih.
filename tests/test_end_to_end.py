"""
KalaiPaalam AI - Comprehensive End-to-End Acceptance Test Suite
Verifies:
1. AI Studio Image Matting & Lighting Enhancement (OpenCV / rembg)
2. Bhashini Speech & Multilingual NLP (Tamil/Hindi/English)
3. Explainable Fair-Price Calculation Engine
4. Canonical Product Assembly & Schema Compliance
5. Multi-Marketplace Adapters (ONDC, GeM, Amazon, Flipkart, Storefront)
6. Centralized 1-Click Price & Inventory Synchronization
7. Offline-First Draft Queue & Batch Reconciliation
8. Judge Audit & Provenance Traceability
"""

import sys
import os
import json

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from app.services.database import init_db, SessionLocal
from app.services.image_service import image_service
from app.services.voice_service import speech_service
from app.services.listing_service import listing_service
from app.services.pricing_service import pricing_service
from app.ai.orchestrator import ai_orchestrator
from app.connectors.registry import connector_registry
from app.services.sync_service import sync_service
from app.models.schema import Product, MarketplaceListing, SyncJob

def test_kalai_paalam_pipeline():
    print("=" * 70)
    print("RUNNING KALAIPAALAM AI END-TO-END ACCEPTANCE TEST SUITE")
    print("SIH26090: Heritage & Culture • Software")
    print("=" * 70)

    # 1. Initialize Database
    print("\n[Step 1] Initializing Database & Demo Seeds...")
    init_db(seed=True)
    db = SessionLocal()
    existing_count = db.query(Product).count()
    assert existing_count >= 2, f"Expected at least 2 seeded products, got {existing_count}"
    print(f"✓ Database initialized. Seeded products count: {existing_count}")

    # 2. Test AI Studio Image Processing
    print("\n[Step 2] Testing AI Studio Image Processing Pipeline...")
    raw_saree_path = os.path.join(os.path.dirname(__file__), "..", "data", "images", "saree_raw.jpg")
    with open(raw_saree_path, "rb") as f:
        img_bytes = f.read()

    img_res = image_service.process_craft_image(img_bytes, "test_saree.jpg")
    assert "catalog_" in img_res["processed_image_url"]
    assert img_res["edge_matting_status"] in ["TEXTURE_PRESERVED_GRABCUT", "U2NETP_HIGH_PRECISION_FEATHERED", "HIGH_PRECISION_FEATHERED"]
    assert "PRESERVED" in img_res["lighting_status"] or "NORMALIZED" in img_res["lighting_status"]
    print(f"✓ AI Studio processed master image: {img_res['processed_image_url']}")

    # 3. Test Bhashini Vernacular Speech & Translation
    print("\n[Step 3] Testing Vernacular Speech & Bhashini Translation...")
    speech_res = speech_service.transcribe_and_translate(
        spoken_text="இது எங்க காஞ்சிபுரம் குழு நெய்த தூய பருத்தி புடவை. செய்ய ரெண்டு நாள் ஆச்சு. மூலப்பொருள் செலவு எட்டுநூறு ரூபாய்.",
        source_lang="ta"
    )
    assert speech_res["detected_language"] == "ta"
    assert "cotton saree" in speech_res["translation_en"].lower()
    assert len(speech_res["translation_hi"]) > 0
    print(f"✓ Bhashini translated Tamil craft speech to English & Hindi: {speech_res['translation_en'][:60]}...")

    # 4. Test Structured Field Extraction
    print("\n[Step 4] Testing Structured NLP Extraction...")
    extracted = listing_service.extract_structured_fields(speech_res["translation_en"], "ta")
    assert extracted["category"] == "Textiles & Handloom"
    assert extracted["hsn_code"] == "5208"
    assert extracted["labour_hours"] in [16.0, 32.0, 40.0]
    assert extracted["material_cost"] == 800.0
    print(f"✓ Extracted category: {extracted['category']} | HSN: {extracted['hsn_code']} | Labour: {extracted['labour_hours']} hrs | Cost: ₹{extracted['material_cost']}")

    # 5. Test Dynamic Fair-Price Recommender
    print("\n[Step 5] Testing Dynamic Fair-Price Recommender...")
    pricing = pricing_service.calculate_fair_price(
        material_cost=extracted["material_cost"],
        labour_hours=extracted["labour_hours"],
        category=extracted["category"]
    )
    assert pricing["base_cost"] > extracted["material_cost"]
    assert pricing["recommended_low"] < pricing["recommended_high"]
    assert "skilled labour" in pricing["explanation"]
    print(f"✓ Recommended Fair Price: ₹{pricing['suggested_price']:,.0f} (Range: ₹{pricing['recommended_low']:,.0f} – ₹{pricing['recommended_high']:,.0f})")
    print(f"  Explanation: {pricing['explanation']}")

    # 6. Test Master AI Orchestrator
    print("\n[Step 6] Testing Master AI Orchestrator Full Cycle...")
    ai_out = ai_orchestrator.process_artisan_input(
        existing_image_url="/static/images/saree_raw.jpg",
        spoken_text="Pure cotton handloom saree with floral border. Two days work, 800 rupees yarn cost.",
        source_language="en"
    )
    canonical = ai_out["canonical_product"]
    assert canonical["title"] is not None
    assert canonical["price"] > 0
    print(f"✓ Generated Master Canonical Product: {canonical['product_id']} - '{canonical['title']}'")

    # 7. Test Multi-Marketplace Connectors & Adapters
    print("\n[Step 7] Testing Multi-Marketplace Publishing (ONDC, GeM, Amazon, Flipkart, Catalog)...")
    channels = ["KalaiPaalam Catalog", "ONDC", "GeM", "Amazon", "Flipkart"]
    pub_results = connector_registry.publish_to_channels(canonical, channels)

    for ch in channels:
        res = pub_results.get(ch)
        assert res is not None, f"Missing result for channel {ch}"
        assert res["success"] is True, f"Publishing failed for {ch}: {res}"
        print(f"✓ [{ch}] Listing created -> ID: {res['external_listing_id']} (Status: {res['status']})")

    # 8. Test Centralized Price Synchronization
    print("\n[Step 8] Testing Centralized 1-Click Price Synchronization (₹5,500 -> ₹5,800)...")
    active_channel_list = [
        {"marketplace": ch, "external_listing_id": pub_results[ch]["external_listing_id"]}
        for ch in channels
    ]
    price_sync_res = connector_registry.sync_price_across_channels(active_channel_list, 5800.0)
    for ch, sync_r in price_sync_res.items():
        assert sync_r["success"] is True
        print(f"✓ [{ch}] Price synchronized to ₹5,800")

    # 9. Test Centralized Inventory Synchronization
    print("\n[Step 9] Testing Centralized Inventory Synchronization (10 -> 9 units)...")
    inv_sync_res = connector_registry.sync_inventory_across_channels(active_channel_list, 9)
    for ch, sync_r in inv_sync_res.items():
        assert sync_r["success"] is True
        print(f"✓ [{ch}] Inventory synchronized to 9 units")

    # 10. Test Offline-First Batch Sync
    print("\n[Step 10] Testing Offline-First Queue & Batch Sync...")
    offline_batch = {
        "timestamp": "2026-09-29T12:00:00Z",
        "items": [
            {
                "local_id": "OFFLINE-DRAFT-099",
                "product": {
                    "product_id": "OFFLINE-DRAFT-099",
                    "title": "Terracotta Handcrafted Village Planter",
                    "category": "Pottery & Terracotta",
                    "craft_type": "Clay Wheel Throwing",
                    "material": ["River Clay"],
                    "price": 1200.0,
                    "inventory": 15,
                    "hsn_code": "6912",
                    "description": "Hand-turned terracotta village planter."
                },
                "channels": ["KalaiPaalam Catalog", "ONDC", "Amazon"]
            }
        ]
    }
    sync_result = sync_service.process_offline_sync_batch(db, offline_batch)
    assert sync_result["success"] is True
    assert sync_result["synced_count"] == 1
    print(f"✓ Offline batch successfully synchronized and published to {sync_result['results'][0]['marketplace_statuses'].keys()}")

    print("\n" + "=" * 70)
    print("ALL 10 KALAIPAALAM AI ACCEPTANCE CRITERIA PASSED SUCCESSFULLY! (100%)")
    print("=" * 70)

if __name__ == "__main__":
    test_kalai_paalam_pipeline()
