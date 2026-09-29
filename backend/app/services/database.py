"""
Database initialization and session management for KalaiPaalam AI.
Supports PostgreSQL through DATABASE_URL or SQLite for local self-contained operation.
"""

import os
import json
import uuid
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.schema import (
    Base, User, ArtisanProfile, Product, ProductImage, Listing,
    PriceRecommendation, MarketplaceConnection, MarketplaceListing,
    SyncJob, InventoryRecord, Consent, AuditLog
)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kalai_paalam.db")

# For SQLite, allow multithreaded access
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db(seed: bool = True):
    """Creates all database tables and seeds demo records if empty."""
    Base.metadata.create_all(bind=engine)
    if seed:
        seed_demo_data()

def seed_demo_data():
    db = SessionLocal()
    try:
        # Check if already seeded
        existing_artisan = db.query(ArtisanProfile).filter_by(id="artisan_demo_01").first()
        if existing_artisan:
            return

        # 1. User & Consent
        user = User(
            id="user_demo_01",
            phone="+91 98765 43210",
            language="ta",
            consent_status=True
        )
        db.add(user)
        
        consent = Consent(
            id="consent_01",
            user_id=user.id,
            consent_type="VOICE_IMAGE_COMMERCE_PROCESSING",
            granted=True
        )
        db.add(consent)

        # 2. Artisan Profile
        artisan = ArtisanProfile(
            id="artisan_demo_01",
            user_id=user.id,
            name="Meenakshi Sundaram",
            craft_type="Handloom Cotton & Silk Weaving",
            location="Kanchipuram, Tamil Nadu",
            cluster_id="cluster_kanchi_04",
            cluster_name="Kanchipuram Heritage Weavers Guild"
        )
        db.add(artisan)

        # 3. Marketplace Connections
        connections = [
            MarketplaceConnection(
                id="conn_ondc",
                artisan_id=artisan.id,
                marketplace="ONDC",
                connection_type="BECKN_PROTOCOL_ADAPTER",
                status="CONNECTED",
                account_name="Kanchi Craft BAP/BPP Node",
                external_account_id="ONDC-NODE-TN-982",
                access_token_reference="vault://ondc-auth-ref-01",
                connected_at=datetime.now(timezone.utc),
                last_synced_at=datetime.now(timezone.utc),
                capabilities_json=json.dumps(["CREATE_LISTING", "UPDATE_PRICE", "UPDATE_INVENTORY", "CATALOG_SEARCH"]),
                environment="DEMO"
            ),
            MarketplaceConnection(
                id="conn_gem",
                artisan_id=artisan.id,
                marketplace="GeM",
                connection_type="GOVT_PROCUREMENT_FEED",
                status="CONNECTED",
                account_name="GeM Artisan Seller Portal",
                external_account_id="GEM-ARTISAN-TN-441",
                access_token_reference="vault://gem-cert-ref-02",
                connected_at=datetime.now(timezone.utc),
                last_synced_at=datetime.now(timezone.utc),
                capabilities_json=json.dumps(["CREATE_LISTING", "UPDATE_INVENTORY", "DIRECT_PURCHASE_FEED"]),
                environment="DEMO"
            ),
            MarketplaceConnection(
                id="conn_amazon",
                artisan_id=artisan.id,
                marketplace="Amazon",
                connection_type="SELLER_PARTNER_API",
                status="CONNECTED",
                account_name="Kanchipuram Karigar Storefront",
                external_account_id="AMZN-SELLER-IN-8891",
                access_token_reference="vault://amz-spapi-ref-03",
                connected_at=datetime.now(timezone.utc),
                last_synced_at=datetime.now(timezone.utc),
                capabilities_json=json.dumps(["CREATE_LISTING", "UPDATE_LISTING", "UPDATE_PRICE", "UPDATE_INVENTORY", "ORDERS", "IMAGE_UPLOAD"]),
                environment="DEMO"
            ),
            MarketplaceConnection(
                id="conn_flipkart",
                artisan_id=artisan.id,
                marketplace="Flipkart",
                connection_type="FLIPKART_SAMARTH_API",
                status="CONNECTED",
                account_name="Samarth Artisan Hub TN",
                external_account_id="FK-SMT-7720",
                access_token_reference="vault://fk-auth-ref-04",
                connected_at=datetime.now(timezone.utc),
                last_synced_at=datetime.now(timezone.utc),
                capabilities_json=json.dumps(["CREATE_LISTING", "UPDATE_PRICE", "UPDATE_INVENTORY"]),
                environment="DEMO"
            ),
            MarketplaceConnection(
                id="conn_storefront",
                artisan_id=artisan.id,
                marketplace="KalaiPaalam Catalog",
                connection_type="NATIVE_D2C_STOREFRONT",
                status="CONNECTED",
                account_name="Official Artisan D2C Store",
                external_account_id="KP-STORE-001",
                access_token_reference="vault://kp-native-ref-05",
                connected_at=datetime.now(timezone.utc),
                last_synced_at=datetime.now(timezone.utc),
                capabilities_json=json.dumps(["CREATE_LISTING", "UPDATE_LISTING", "UPDATE_PRICE", "UPDATE_INVENTORY", "ORDERS", "IMAGE_UPLOAD"]),
                environment="LIVE"
            )
        ]
        for conn in connections:
            db.add(conn)

        # 4. Canonical Product 1 - Handwoven Cotton Saree
        p1 = Product(
            id="KP-001",
            artisan_id=artisan.id,
            title="Handwoven Cotton Floral Border Saree",
            hindi_title="पारंपरिक फ्लोरल बॉर्डर वाली हथकरघा सूती साड़ी",
            tamil_title="கைத்தறி பருத்தி பூ வேலைப்பாடு சேலை",
            category="Textiles & Handloom",
            subcategory="Saree",
            craft_type="Handloom Weaving",
            material=json.dumps(["Pure Cotton", "Organic Dye"]),
            colors=json.dumps(["Indigo Blue", "Deep Maroon"]),
            description="Exquisitely handwoven cotton saree crafted over 40 hours using heritage pit-loom techniques. Features an intricate traditional floral temple border with natural vegetable dyed threads, offering exceptional breathability and timeless elegance.",
            hindi_description="40 घंटे से अधिक समय में पारंपरिक गड्ढा-करघा तकनीकों से बुनी गई शुद्ध सूती साड़ी। इसमें प्राकृतिक रंगों से रंगे धागों के साथ एक जटिल पारंपरिक पुष्प मंदिर बॉर्डर है।",
            dimensions_json=json.dumps({"length_cm": 550, "width_cm": 115, "height_cm": 1}),
            weight_grams=520.0,
            hsn_code="5208",
            country_of_origin="India",
            labour_hours=40.0,
            material_cost=800.0,
            labour_rate=120.0,
            overhead=200.0,
            market_signal=1.12,
            price=5500.0,
            inventory=10,
            sku="KP-HL-COT-001",
            original_image_url="/static/images/saree_raw.jpg",
            processed_image_url="/static/images/saree_catalog.jpg",
            voice_transcript="This is a handwoven cotton saree made by our group in Kanchipuram. It has a traditional floral border with blue and maroon colours, and took about two days of continuous pit loom work. The yarn and dye material cost was around eight hundred rupees.",
            detected_language="ta",
            craft_story="Woven by 3rd-generation artisan Meenakshi Sundaram preserving 120-year-old family motifs from Kanchipuram weaving tradition.",
            confidence_score="HIGH",
            provenance_json=json.dumps({
                "material": "VOICE",
                "labour_hours": "ARTISAN",
                "category": "AI_SUGGESTED",
                "price": "PRICE_ENGINE",
                "description": "AI_GENERATED"
            }),
            status="PUBLISHED"
        )
        db.add(p1)

        # Price Recommendation for P1
        # BaseCost = 800 + (40 * 120) + 200 = 800 + 4800 + 200 = 5800
        # MarketAdjusted = 5800 * 1.12 = 6496 -> Range: 5200 - 5800
        pr1 = PriceRecommendation(
            id="price_rec_01",
            product_id=p1.id,
            material_cost=800.0,
            labour_hours=40.0,
            labour_rate=120.0,
            overhead=200.0,
            market_signal=1.12,
            base_cost=5800.0,
            recommended_low=5200.0,
            recommended_mid=5500.0,
            recommended_high=5900.0,
            explanation="Calculated from declared raw yarn & organic dye cost (₹800), 40 skilled handloom labour hours @ ₹120/hr benchmark, ₹200 packaging & local transport overhead, and 1.12x festive handloom market signal."
        )
        db.add(pr1)

        # Listing for P1
        l1 = Listing(
            id="list_01",
            product_id=p1.id,
            english_title=p1.title,
            english_description=p1.description,
            hindi_title=p1.hindi_title,
            hindi_description=p1.hindi_description,
            bullet_points_json=json.dumps([
                "100% Authentic Handloom Pure Cotton Saree",
                "Woven on traditional pit-looms in Kanchipuram",
                "Intricate floral temple border with natural vegetable dyes",
                "Includes unstitched matching blouse piece (80 cm)",
                "Gentle handwash in cold water recommended"
            ]),
            keywords=json.dumps(["handloom saree", "kanchipuram cotton", "traditional floral border", "organic dye saree", "artisan handwoven"]),
            seo_tags=json.dumps(["handloom", "saree", "kanchipuram", "ethical fashion", "zero-middleman"])
        )
        db.add(l1)

        # Marketplace Listings for P1 (Already published to multi-channels)
        m_listings = [
            MarketplaceListing(
                id="ml_01",
                product_id=p1.id,
                marketplace="ONDC",
                external_listing_id="ONDC-KP-001-ITEM",
                status="PUBLISHED",
                listing_url="https://ondc.org/catalog/KP-001",
                last_synced_at=datetime.now(timezone.utc)
            ),
            MarketplaceListing(
                id="ml_02",
                product_id=p1.id,
                marketplace="GeM",
                external_listing_id="GEM-CAT-2026-001",
                status="PUBLISHED",
                listing_url="https://gem.gov.in/products/KP-001",
                last_synced_at=datetime.now(timezone.utc)
            ),
            MarketplaceListing(
                id="ml_03",
                product_id=p1.id,
                marketplace="Amazon",
                external_listing_id="DEMO-AMZ-KP001",
                status="PUBLISHED",
                listing_url="https://amazon.in/dp/DEMO-AMZ-KP001",
                last_synced_at=datetime.now(timezone.utc)
            ),
            MarketplaceListing(
                id="ml_04",
                product_id=p1.id,
                marketplace="Flipkart",
                external_listing_id="DEMO-FK-KP001",
                status="PUBLISHED",
                listing_url="https://flipkart.com/p/DEMO-FK-KP001",
                last_synced_at=datetime.now(timezone.utc)
            ),
            MarketplaceListing(
                id="ml_05",
                product_id=p1.id,
                marketplace="KalaiPaalam Catalog",
                external_listing_id="KP-STORE-001",
                status="PUBLISHED",
                listing_url="/catalog/KP-001",
                last_synced_at=datetime.now(timezone.utc)
            )
        ]
        for ml in m_listings:
            db.add(ml)

        # Inventory
        inv1 = InventoryRecord(
            id="inv_01",
            product_id=p1.id,
            total_stock=10,
            reserved_stock=0,
            available_stock=10
        )
        db.add(inv1)

        # Canonical Product 2 - Dhokra Peacock Brass Lamp
        p2 = Product(
            id="KP-002",
            artisan_id=artisan.id,
            title="Handcrafted Dhokra Brass Peacock Lamp",
            hindi_title="हस्तनिर्मित ढोकरा पीतल मयूर दीया / दीपक",
            tamil_title="பாரம்பரிய தோக்ரா பித்தளை மயில் விளக்கு",
            category="Metalware & Brass",
            subcategory="Oil Lamp / Diya",
            craft_type="Lost-Wax Dhokra Metal Casting",
            material=json.dumps(["Brass", "Clay Core", "Beeswax"]),
            colors=json.dumps(["Antique Gold", "Verdigris Patina"]),
            description="Ancient 4000-year-old lost-wax bell metal casting technique producing a ceremonial peacock diya. Preserves rustic textures and hand-coiled beeswax thread detailing.",
            hindi_description="4000 साल पुरानी लुप्त-मोम ढोकरा धातु ढलाई तकनीक से निर्मित मयूर दीया। हस्तनिर्मित बनावट और पारंपरिक रूप से समृद्ध।",
            dimensions_json=json.dumps({"length_cm": 15, "width_cm": 12, "height_cm": 22}),
            weight_grams=850.0,
            hsn_code="7419",
            country_of_origin="India",
            labour_hours=24.0,
            material_cost=550.0,
            labour_rate=120.0,
            overhead=150.0,
            market_signal=1.20,
            price=3800.0,
            inventory=8,
            sku="KP-MET-DKR-002",
            original_image_url="/static/images/brass_raw.jpg",
            processed_image_url="/static/images/brass_catalog.jpg",
            voice_transcript="This is a dhokra brass oil lamp with peacock motif, made using lost wax casting. It took about three days. Brass raw metal cost was around five hundred and fifty rupees.",
            detected_language="hi",
            craft_story="Preserving prehistoric non-ferrous metal casting passed down through generations of tribal metalworkers.",
            confidence_score="HIGH",
            provenance_json=json.dumps({"material": "VOICE", "labour_hours": "ARTISAN", "price": "PRICE_ENGINE"}),
            status="PUBLISHED"
        )
        db.add(p2)

        inv2 = InventoryRecord(
            id="inv_02",
            product_id=p2.id,
            total_stock=8,
            reserved_stock=0,
            available_stock=8
        )
        db.add(inv2)

        # Sync jobs history
        sync1 = SyncJob(
            id="sync_job_01",
            product_id=p1.id,
            marketplace="ONDC",
            operation="CREATE_LISTING",
            status="SUCCESS",
            external_id="ONDC-KP-001-ITEM"
        )
        sync2 = SyncJob(
            id="sync_job_02",
            product_id=p1.id,
            marketplace="Amazon",
            operation="UPDATE_PRICE",
            status="SUCCESS",
            external_id="DEMO-AMZ-KP001"
        )
        db.add(sync1)
        db.add(sync2)

        # Audit log
        db.add(AuditLog(
            id=str(uuid.uuid4()),
            entity_type="SYSTEM",
            entity_id="INIT",
            action="BOOTSTRAP",
            actor="SYSTEM",
            details="KalaiPaalam AI database seeded with demo artisan and canonical products."
        ))

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()
