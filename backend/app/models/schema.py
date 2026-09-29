"""
KalaiPaalam AI - Database Models & Schema
Supports PostgreSQL and SQLite (fallback / local testing).
Implements all 16 canonical relational entities required by SIH26090 specification.
"""

import json
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, create_engine
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import os

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String(64), primary_key=True)
    phone = Column(String(20), nullable=True)
    language = Column(String(10), default="ta")  # ta, hi, en
    consent_status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    profiles = relationship("ArtisanProfile", back_populates="user")
    consents = relationship("Consent", back_populates="user")

class ArtisanProfile(Base):
    __tablename__ = "artisan_profiles"
    id = Column(String(64), primary_key=True)
    user_id = Column(String(64), ForeignKey("users.id"))
    name = Column(String(128))
    craft_type = Column(String(128))
    location = Column(String(128))
    cluster_id = Column(String(64), nullable=True)
    cluster_name = Column(String(128), default="Kanchipuram Silk & Cotton Weavers Guild")

    user = relationship("User", back_populates="profiles")
    products = relationship("Product", back_populates="artisan")

class Product(Base):
    __tablename__ = "products"
    id = Column(String(64), primary_key=True)
    artisan_id = Column(String(64), ForeignKey("artisan_profiles.id"))
    title = Column(String(256), nullable=False)
    hindi_title = Column(String(256), nullable=True)
    tamil_title = Column(String(256), nullable=True)
    category = Column(String(128), default="Textiles & Handloom")
    subcategory = Column(String(128), default="Saree")
    craft_type = Column(String(128), default="Handwoven Jacquard")
    material = Column(Text, default="[\"Cotton\"]")  # JSON encoded list
    colors = Column(Text, default="[\"Blue\", \"Maroon\"]")  # JSON encoded list
    description = Column(Text, nullable=True)
    hindi_description = Column(Text, nullable=True)
    tamil_description = Column(Text, nullable=True)
    dimensions_json = Column(Text, default="{}")  # length, width, height
    weight_grams = Column(Float, default=450.0)
    hsn_code = Column(String(32), default="5208")
    country_of_origin = Column(String(64), default="India")
    
    # Financials & Fair Price
    labour_hours = Column(Float, default=16.0)
    material_cost = Column(Float, default=450.0)
    labour_rate = Column(Float, default=120.0)
    overhead = Column(Float, default=150.0)
    market_signal = Column(Float, default=1.15)
    price = Column(Float, default=5500.0)
    inventory = Column(Integer, default=10)
    sku = Column(String(64), nullable=True)
    
    # Imagery & Audio
    original_image_url = Column(String(512), nullable=True)
    processed_image_url = Column(String(512), nullable=True)
    voice_transcript = Column(Text, nullable=True)
    detected_language = Column(String(10), default="ta")
    craft_story = Column(Text, nullable=True)
    
    # AI Metadata & Confidence
    confidence_score = Column(String(16), default="HIGH")  # HIGH, MEDIUM, LOW
    provenance_json = Column(Text, default="{}")  # Field sources
    status = Column(String(32), default="READY")  # DRAFT, PENDING_AI, READY, APPROVED, PUBLISHED, PENDING_SYNC, FAILED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    artisan = relationship("ArtisanProfile", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    listings = relationship("Listing", back_populates="product", cascade="all, delete-orphan")
    marketplace_listings = relationship("MarketplaceListing", back_populates="product", cascade="all, delete-orphan")
    sync_jobs = relationship("SyncJob", back_populates="product", cascade="all, delete-orphan")

class ProductImage(Base):
    __tablename__ = "product_images"
    id = Column(String(64), primary_key=True)
    product_id = Column(String(64), ForeignKey("products.id"))
    original_url = Column(String(512))
    processed_url = Column(String(512), nullable=True)
    thumbnail_url = Column(String(512), nullable=True)
    edge_matting_status = Column(String(32), default="COMPLETED")
    lighting_status = Column(String(32), default="ENHANCED")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    product = relationship("Product", back_populates="images")

class VoiceInput(Base):
    __tablename__ = "voice_inputs"
    id = Column(String(64), primary_key=True)
    product_id = Column(String(64), ForeignKey("products.id"), nullable=True)
    language = Column(String(10), default="ta")
    audio_url = Column(String(512), nullable=True)
    raw_transcript = Column(Text)
    translation_en = Column(Text, nullable=True)
    translation_hi = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ProductAttribute(Base):
    __tablename__ = "product_attributes"
    id = Column(String(64), primary_key=True)
    product_id = Column(String(64), ForeignKey("products.id"))
    attribute_name = Column(String(64))
    attribute_value = Column(String(256))
    source = Column(String(32))  # VOICE, ARTISAN, AI_SUGGESTED, MANUAL_EDIT
    confidence = Column(String(16), default="HIGH")

class Listing(Base):
    __tablename__ = "listings"
    id = Column(String(64), primary_key=True)
    product_id = Column(String(64), ForeignKey("products.id"))
    english_title = Column(String(256))
    english_description = Column(Text)
    hindi_title = Column(String(256), nullable=True)
    hindi_description = Column(Text, nullable=True)
    bullet_points_json = Column(Text, default="[]")
    keywords = Column(Text, default="[]")  # JSON array
    seo_tags = Column(Text, default="[]")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    product = relationship("Product", back_populates="listings")

class PriceRecommendation(Base):
    __tablename__ = "price_recommendations"
    id = Column(String(64), primary_key=True)
    product_id = Column(String(64), ForeignKey("products.id"))
    material_cost = Column(Float)
    labour_hours = Column(Float)
    labour_rate = Column(Float)
    overhead = Column(Float)
    market_signal = Column(Float)
    base_cost = Column(Float)
    recommended_low = Column(Float)
    recommended_mid = Column(Float)
    recommended_high = Column(Float)
    explanation = Column(Text)
    model_version = Column(String(64), default="FairPrice-Heuristic-v1.2")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class MarketplaceConnection(Base):
    __tablename__ = "marketplace_connections"
    id = Column(String(64), primary_key=True)
    artisan_id = Column(String(64), default="demo_artisan_1")
    marketplace = Column(String(64))  # ONDC, GeM, Amazon, Flipkart, Storefront
    connection_type = Column(String(32), default="OAUTH_TOKEN")
    status = Column(String(32), default="CONNECTED")  # NOT_CONNECTED, CONNECTING, CONNECTED, AUTH_REQUIRED, EXPIRED, ERROR, DISCONNECTED, SANDBOX, DEMO
    account_name = Column(String(128))
    external_account_id = Column(String(128), nullable=True)
    access_token_reference = Column(String(128), nullable=True)  # Secure token vault reference, NEVER raw secret
    refresh_token_reference = Column(String(128), nullable=True)
    connected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_synced_at = Column(DateTime, nullable=True)
    capabilities_json = Column(Text, default="[]")  # e.g. ["CREATE_LISTING", "UPDATE_PRICE", "UPDATE_INVENTORY"]
    environment = Column(String(16), default="DEMO")  # LIVE, SANDBOX, DEMO, UNAVAILABLE

class MarketplaceListing(Base):
    __tablename__ = "marketplace_listings"
    id = Column(String(64), primary_key=True)
    product_id = Column(String(64), ForeignKey("products.id"))
    marketplace = Column(String(64))
    external_listing_id = Column(String(128))
    status = Column(String(32), default="PUBLISHED")  # PUBLISHED, PENDING, BLOCKED, FAILED, UPDATING
    listing_url = Column(String(512), nullable=True)
    last_synced_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_error = Column(Text, nullable=True)

    product = relationship("Product", back_populates="marketplace_listings")

class MarketplacePayload(Base):
    __tablename__ = "marketplace_payloads"
    id = Column(String(64), primary_key=True)
    product_id = Column(String(64), ForeignKey("products.id"))
    target = Column(String(64))  # ondc, gem, amazon, flipkart, storefront
    payload_json = Column(Text)
    status = Column(String(32), default="GENERATED")  # GENERATED, SENT, VALIDATION_ERROR
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class SyncJob(Base):
    __tablename__ = "sync_jobs"
    id = Column(String(64), primary_key=True)
    product_id = Column(String(64), ForeignKey("products.id"), nullable=True)
    marketplace = Column(String(64))
    operation = Column(String(32))  # CREATE_LISTING, UPDATE_PRICE, UPDATE_INVENTORY, SYNC_CATALOG
    status = Column(String(32), default="SUCCESS")  # QUEUED, PROCESSING, SUCCESS, FAILED, RETRYING, BLOCKED
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
    retry_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    external_id = Column(String(128), nullable=True)

    product = relationship("Product", back_populates="sync_jobs")

class InventoryRecord(Base):
    __tablename__ = "inventory"
    id = Column(String(64), primary_key=True)
    product_id = Column(String(64), ForeignKey("products.id"))
    total_stock = Column(Integer, default=10)
    reserved_stock = Column(Integer, default=0)
    available_stock = Column(Integer, default=10)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class OrderRecord(Base):
    __tablename__ = "orders"
    id = Column(String(64), primary_key=True)
    external_order_id = Column(String(128))
    marketplace = Column(String(64))
    product_id = Column(String(64), ForeignKey("products.id"))
    product_title = Column(String(256), nullable=True)
    quantity = Column(Integer, default=1)
    amount = Column(Float, default=0.0)
    buyer_name = Column(String(128), default="Verified Buyer")
    shipping_status = Column(String(32), default="CONFIRMED")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Consent(Base):
    __tablename__ = "consents"
    id = Column(String(64), primary_key=True)
    user_id = Column(String(64), ForeignKey("users.id"))
    consent_type = Column(String(64), default="DATA_PROCESSING_VOICE_IMAGE")
    granted = Column(Boolean, default=True)
    ip_address = Column(String(45), default="127.0.0.1")
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="consents")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String(64), primary_key=True)
    entity_type = Column(String(64))
    entity_id = Column(String(64))
    action = Column(String(64))  # CREATE, UPDATE, SYNC, PUBLISH, OVERRIDE
    actor = Column(String(64), default="ARTISAN")
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
