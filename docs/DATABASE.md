# Database Architecture & Entity Relational Schema

## 1. Relational Entities (16 Core Tables)
KalaiPaalam AI implements an enterprise-grade schema supporting both PostgreSQL in production and SQLite for local self-contained deployment.

1. **`users`**: Artisan and administrative user credentials, preferred language, consent status.
2. **`artisan_profiles`**: Artisan biographical details, craft discipline, location, cluster association.
3. **`products`**: Master canonical craft products with bilingual titles, craft stories, dimensions, and financial baselines.
4. **`product_images`**: Raw original photos, AI Studio processed catalog images, matting status, lighting metrics.
5. **`voice_inputs`**: Spoken audio URL, raw transcript, English and Hindi translations.
6. **`product_attributes`**: Normalized craft attributes with source provenance and confidence levels.
7. **`listings`**: Multi-lingual product copy (English + Hindi), SEO tags, and bullet points.
8. **`price_recommendations`**: Cost baseline breakdown (material + labour + overhead), market multipliers, explainable reasoning.
9. **`marketplace_connections`**: Channels (ONDC, GeM, Amazon, Flipkart, Catalog), OAuth token vault references, capabilities, environments.
10. **`marketplace_listings`**: Channel-specific listing status, external IDs, and URLs.
11. **`marketplace_payloads`**: Exact generated protocol JSON payloads (Beckn BPP, GeM feed, SP-API).
12. **`sync_jobs`**: Job queue tracking operations (`CREATE_LISTING`, `UPDATE_PRICE`, `UPDATE_INVENTORY`), retry attempts, and errors.
13. **`inventory`**: Central stock allocation, available units, and reservations.
14. **`orders`**: Incoming channel orders, buyer data, and fulfillment state.
15. **`consents`**: DPDP-aligned data capture consent audit trail.
16. **`audit_logs`**: System event logs capturing changes, human overrides, and publishing operations.
