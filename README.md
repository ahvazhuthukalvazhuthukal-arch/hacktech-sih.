# KalaiPaalam AI 🏛️
### Smart India Hackathon 2026 — SIH26090
**Theme:** Heritage & Culture | **Category:** Software  
**Core Innovation:** *One Artisan → One Digital Product → Many Marketplaces*

---

## 🌟 Executive Summary

Marginalized rural artisans possess extraordinary craft heritage but face insurmountable friction in photography, digital cataloging, English descriptions, pricing, and managing fragmented e-commerce seller portals.

**KalaiPaalam AI removes that digital burden.**

```
                     ARTISAN
                        │
                  PHOTO + VOICE
                        │
                        ▼
                KALAIPAALAM AI
                        │
                CANONICAL PRODUCT
                        │
               MARKETPLACE ENGINE
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
      ONDC             GeM           AMAZON
  (Beckn BPP)     (Procurement)     (SP-API)
        │               │               │
        └───────────────┼───────────────┘
                        ▼
                     FLIPKART
                     (Samarth)
                        │
                        ▼
                  D2C STOREFRONT
```

An artisan creates a product **only once**. KalaiPaalam converts spoken descriptions and photos into a master canonical product, calculates an explainable fair price, and projects it into destination schemas across **ONDC, GeM, Amazon Karigar, Flipkart Samarth, and D2C Storefront**.

---

## 🚀 Key Architectural Highlights

1. **AI Studio Image Processing**: OpenCV GrabCut edge matting and CLAHE lighting normalization remove messy workshop backgrounds while preserving delicate handloom weaves, zari threads, and brass luster.
2. **Vernacular Speech & NLP (Bhashini-First)**: Speaks in Tamil, Hindi, or English. Converts unscripted craft narratives into structured JSON with zero typing.
3. **Dynamic Fair-Price Engine**: Transparent baseline formula:
   $$\text{BaseCost} = \text{MaterialCost} + (\text{LabourHours} \times \text{LabourRate}) + \text{Overhead}$$
   $$\text{MarketAdjusted} = \text{BaseCost} \times \text{MarketSignalMultiplier}$$
4. **Decoupled Marketplace Connectors**: The mobile client **never** talks directly to external marketplaces. The backend Connector Layer handles authentication, field mapping, pre-publish validation, and token vaulting.
5. **Centralized 1-Click Sync**: Updating a price from ₹5,500 to ₹5,800 or decrementing stock propagates across all 5 connected stores simultaneously.
6. **Offline-First Resilience**: Local SQLite caching retains drafts and audio recordings with status `PENDING_SYNC`, automatically reconciling when internet returns.
7. **Village Cluster Mode**: Cluster managers can bulk-publish 50+ products across national channels in one click.

---

## 📂 Repository Structure

```
kalai-paalam/
├── mobile/                  # Complete Flutter mobile codebase (clean architecture)
│   ├── lib/
│   │   ├── main.dart        # Splash, Consent, and Routes
│   │   ├── models/          # CanonicalProduct model
│   │   ├── services/        # ApiClient
│   │   ├── storage/         # SQLite offline database
│   │   └── features/        # Home, Camera, AI Review, Pricing, Marketplaces, Stores
│   └── pubspec.yaml
├── backend/                 # FastAPI backend & AI services
│   ├── app/
│   │   ├── main.py          # Entrypoint mounting all routers & static PWA console
│   │   ├── api/             # Products, Marketplaces, Media, Sync, Admin, Catalog
│   │   ├── ai/              # AI Pipeline Orchestrator
│   │   ├── services/        # ImageService, VoiceService, ListingService, PricingService, Database
│   │   ├── models/          # SQLAlchemy schema (16 tables)
│   │   ├── connectors/      # ONDC, GeM, Amazon, Flipkart, Storefront, Demo adapters
│   │   └── static/          # High-fidelity Web & Mobile PWA Demo Console (index.html)
├── data/                    # Seed datasets (products, prices, sample transcripts, images)
├── docs/                    # Complete SIH technical documentation
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── MARKETPLACE_CONNECTORS.md
│   ├── MCP_INTEGRATION.md
│   ├── AI_PIPELINE.md
│   ├── OFFLINE_ARCHITECTURE.md
│   ├── DATABASE.md
│   ├── DEMO_GUIDE.md
│   ├── LIMITATIONS.md
│   └── JUDGE_QA.md
├── scripts/                 # Server runners & demo generators
│   └── run_backend.py
├── tests/                   # Acceptance test suite
│   └── test_end_to_end.py
├── docker-compose.yml       # PostgreSQL, Redis & FastAPI orchestration
└── README.md
```

---

## ⚡ Quickstart & Testing

### 1. Run the End-to-End Acceptance Tests
Verify all 10 core pipeline stages (AI Studio, Bhashini speech, pricing engine, canonical mapping, multi-channel publishing, price sync, inventory sync, offline sync):
```bash
python tests/test_end_to_end.py
```
*Expected Result: 10/10 Acceptance Tests Passed (100%)*

### 2. Start the Backend & Interactive Console
```bash
python scripts/run_backend.py
```
Open **[http://localhost:8000](http://localhost:8000)** in any browser.

You can interactively evaluate:
* 📱 **Artisan Mobile App**: Capture photo, record voice, inspect AI Studio image matting, review touch-to-confirm cards, and 1-click publish across channels.
* 🔌 **Connect Your Stores**: Manage ONDC, GeM, Amazon, and Flipkart connections and inspect operational capabilities.
* 🔄 **Multi-Store Sync**: Change price or inventory once and watch real-time updates broadcast to all channels.
* 📊 **Admin & Judge Traceability**: Inspect the raw audit trail from voice waveform to JSON payloads.
* 🛍️ **Buyer Catalog**: Browse products by craft, view artisan stories, and place direct D2C orders.
* 📖 **Swagger API Docs**: Visit **[http://localhost:8000/docs](http://localhost:8000/docs)**.

---

## 🏆 SIH26090 Evaluation Criteria Compliance

| SIH PPT Requirement | Working Implementation | Documentation Reference |
| :--- | :--- | :--- |
| **AI Studio** | OpenCV GrabCut foreground matting + CLAHE lighting normalization + neutral drop shadow. | [AI_PIPELINE.md](file:///C:/Users/ANDREWS/.gemini/antigravity/scratch/kalai-paalam/docs/AI_PIPELINE.md) |
| **Voice-to-Listing NLP** | Bhashini speech transcription & translation; bilingual English + Hindi copy. | [AI_PIPELINE.md](file:///C:/Users/ANDREWS/.gemini/antigravity/scratch/kalai-paalam/docs/AI_PIPELINE.md) |
| **Dynamic Fair Price** | Explainable formula based on raw materials, skilled labour hours, and market signals. | [AI_PIPELINE.md](file:///C:/Users/ANDREWS/.gemini/antigravity/scratch/kalai-paalam/docs/AI_PIPELINE.md) |
| **Zero-Typing UX** | Touch-to-confirm cards with source provenance labels. | [DEMO_GUIDE.md](file:///C:/Users/ANDREWS/.gemini/antigravity/scratch/kalai-paalam/docs/DEMO_GUIDE.md) |
| **ONDC-Native Linkage** | Protocol adapter generating compliant Beckn BPP Item catalog schemas. | [MARKETPLACE_CONNECTORS.md](file:///C:/Users/ANDREWS/.gemini/antigravity/scratch/kalai-paalam/docs/MARKETPLACE_CONNECTORS.md) |
| **GeM Buyer Feed** | Compliant XML/JSON procurement feed with Make-in-India compliance. | [MARKETPLACE_CONNECTORS.md](file:///C:/Users/ANDREWS/.gemini/antigravity/scratch/kalai-paalam/docs/MARKETPLACE_CONNECTORS.md) |
| **Offline-First Resilience** | Mobile SQLite caching with `PENDING_SYNC` state and automatic batch sync. | [OFFLINE_ARCHITECTURE.md](file:///C:/Users/ANDREWS/.gemini/antigravity/scratch/kalai-paalam/docs/OFFLINE_ARCHITECTURE.md) |
| **Budget Android Support** | Client-side compression (max 1024x1024) keeping memory footprint under 85MB. | [ARCHITECTURE.md](file:///C:/Users/ANDREWS/.gemini/antigravity/scratch/kalai-paalam/docs/ARCHITECTURE.md) |
