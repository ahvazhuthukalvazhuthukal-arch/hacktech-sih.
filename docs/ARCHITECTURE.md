# KalaiPaalam AI — System Architecture Specification

## 1. High-Level Concept: One Artisan → One Digital Product → Many Marketplaces

The core insight of **KalaiPaalam AI** is that marginalized Indian artisans know their craft intimately but face insurmountable digital friction when forced to learn multiple fragmented e-commerce portals.

Rather than forcing the artisan to become a digital cataloger:
1. The artisan captures **one photo** and **speaks in their regional dialect** (Tamil, Hindi, etc.).
2. The AI Studio executes background removal and lighting normalization while preserving delicate textures (zari threads, handloom weaves, brass reflections).
3. The Speech/NLP layer (Bhashini-first) extracts structured attributes and generates bilingual listings (English + Hindi).
4. The Dynamic Fair-Price Recommender computes an explainable price range based on raw materials, skilled labour hours, and market signals.
5. The artisan reviews and confirms with **zero typing**.
6. The product is assembled into a single **Canonical Product Model**.
7. The **Marketplace Engine** projects the canonical product into destination schemas across **ONDC (Beckn protocol), GeM (Government e-Marketplace), Amazon Karigar, Flipkart Samarth, and D2C Storefront**.

```
                  ARTISAN
                     │
                     ▼
             FLUTTER MOBILE APP
                     │
           ┌─────────┴─────────┐
           │                   │
        CAMERA               VOICE
           │                   │
           ▼                   ▼
      IMAGE SERVICE       SPEECH SERVICE
    (OpenCV / rembg)        (Bhashini)
           │                   │
           └─────────┬─────────┘
                     ▼
              AI ORCHESTRATOR
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       LISTING     PRICING    PRODUCT
      GENERATION   ENGINE    EXTRACTION
          │          │          │
          └──────────┼──────────┘
                     ▼
             CANONICAL PRODUCT
                     │
                     ▼
            MARKETPLACE ENGINE
                     │
       ┌─────────────┼──────────────┐
       ▼             ▼              ▼
     ONDC           GeM          AMAZON
  (Beckn BPP)  (Procurement)   (SP-API)
       │             │              │
       └─────────────┼──────────────┘
                     ▼
                  FLIPKART
                  (Samarth)
                     │
                     ▼
               D2C STOREFRONT
```

---

## 2. Core Architectural Rules

### Rule 1: Never Call Marketplaces Directly from Mobile
Mobile devices talk **only** to the KalaiPaalam backend API. Third-party marketplace authentication tokens, protocol payloads, and retry queues are governed server-side in secure vaults.

### Rule 2: Strict Environment Labeling
Every marketplace connector exposes an environment attribute:
* `LIVE`: Production API with live order/publishing capabilities.
* `SANDBOX`: Verified sandbox credentials with mock protocol exchange.
* `DEMO`: Self-contained interactive simulator enabling fail-safe hackathon demonstrations.
* `UNAVAILABLE`: Channel is registered but currently unconfigured.

### Rule 3: Explainable Pricing with Human Agency
AI never dictates the final price. The system outputs an explainable cost breakdown (`BaseCost = Material + Labour + Overhead`) and suggests a bounded range. The artisan maintains absolute authority to approve or override.

### Rule 4: Offline-First SQLite Local Caching
When internet connectivity drops, products and audio recordings are saved locally with status `PENDING_SYNC`. When connection is restored, background idempotent batch synchronization reconciles data with the server.
