"""
KalaiPaalam AI - Master Pipeline Orchestrator
Coordinates the 4 AI stages:
Stage 1: Image Processing (AI Studio)
Stage 2: Vernacular Speech & Translation (Bhashini)
Stage 3: Structured Extraction & Listing Copy
Stage 4: Explainable Fair-Price Recommendation
"""

import uuid
import json
from typing import Dict, Any, Optional
from app.services.image_service import image_service
from app.services.voice_service import speech_service
from app.services.listing_service import listing_service
from app.services.pricing_service import pricing_service

class AIOrchestrator:
    def process_artisan_input(
        self,
        image_bytes: Optional[bytes] = None,
        image_filename: Optional[str] = None,
        existing_image_url: Optional[str] = None,
        voice_bytes: Optional[bytes] = None,
        spoken_text: Optional[str] = None,
        source_language: str = "ta"
    ) -> Dict[str, Any]:
        """
        Executes end-to-end AI transformation:
        Raw Photo + Spoken Voice -> Professional Catalog Image + Bilingual Listing + Fair Price.
        """
        # --- STAGE 1: AI STUDIO IMAGE PROCESSING ---
        if image_bytes:
            img_result = image_service.process_craft_image(image_bytes, image_filename)
            original_img = img_result["original_image_url"]
            processed_img = img_result["processed_image_url"]
            matting_status = img_result["edge_matting_status"]
            lighting_status = img_result["lighting_status"]
        elif existing_image_url:
            original_img = existing_image_url
            processed_img = existing_image_url
            matting_status = "PRE_PROCESSED"
            lighting_status = "PRE_PROCESSED"
        else:
            # Fallback to realistic saree sample for demo reliability
            original_img = "/static/images/saree_raw.jpg"
            processed_img = "/static/images/saree_catalog.jpg"
            matting_status = "TEXTURE_PRESERVED_GRABCUT"
            lighting_status = "CLAHE_GRAYWORLD_NORMALIZED"

        # --- STAGE 2: VERNACULAR SPEECH & TRANSLATION ---
        speech_result = speech_service.transcribe_and_translate(
            audio_data=voice_bytes,
            spoken_text=spoken_text,
            source_lang=source_language
        )
        raw_transcript = speech_result["raw_transcript"]
        transcript_en = speech_result["translation_en"]
        transcript_hi = speech_result["translation_hi"]
        detected_lang = speech_result["detected_language"]

        # --- STAGE 3: STRUCTURED EXTRACTION & BILINGUAL LISTING ---
        extracted = listing_service.extract_structured_fields(
            transcript_en,
            detected_lang,
            image_filename=image_filename
        )

        # --- STAGE 4: EXPLAINABLE FAIR-PRICE RECOMMENDATION ---
        price_result = pricing_service.calculate_fair_price(
            material_cost=extracted["material_cost"],
            labour_hours=extracted["labour_hours"],
            category=extracted["category"]
        )

        product_id = f"KP-{uuid.uuid4().hex[:6].upper()}"

        # Combine into Master Canonical Product
        canonical_product = {
            "product_id": product_id,
            "title": extracted["title"],
            "tamil_title": extracted.get("tamil_title", ""),
            "hindi_title": extracted["hindi_title"],
            "category": extracted["category"],
            "subcategory": extracted["subcategory"],
            "craft_type": extracted["craft_type"],
            "material": extracted["material"],
            "colors": extracted["colors"],
            "dimensions": extracted["dimensions"],
            "weight_grams": extracted["weight_grams"],
            "hsn_code": extracted["hsn_code"],
            "country_of_origin": extracted["country_of_origin"],
            "description": extracted["description"],
            "tamil_description": extracted.get("tamil_description", ""),
            "hindi_description": extracted["hindi_description"],
            "bullet_points": extracted["bullet_points"],
            "keywords": extracted["keywords"],
            "labour_hours": extracted["labour_hours"],
            "material_cost": extracted["material_cost"],
            "price": price_result["suggested_price"],
            "recommended_price_range": {
                "low": price_result["recommended_low"],
                "mid": price_result["recommended_mid"],
                "high": price_result["recommended_high"],
                "explanation": price_result["explanation"]
            },
            "inventory": 10,
            "sku": f"SKU-{product_id}",
            "original_image_url": original_img,
            "processed_image_url": processed_img,
            "voice_transcript": raw_transcript,
            "detected_language": detected_lang,
            "craft_story": f"Handcrafted by rural artisans with heritage {extracted['craft_type']}.",
            "confidence_scores": extracted["confidence_scores"],
            "provenance": extracted["provenance"],
            "status": "READY"
        }

        return {
            "canonical_product": canonical_product,
            "image_metadata": {
                "original_url": original_img,
                "processed_url": processed_img,
                "edge_matting": matting_status,
                "lighting": lighting_status
            },
            "speech_metadata": speech_result,
            "pricing_metadata": price_result
        }

ai_orchestrator = AIOrchestrator()
